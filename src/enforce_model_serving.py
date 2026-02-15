import logging
from pyspark.sql import SparkSession
from pyspark.dbutils import DBUtils
from databricks.sdk import WorkspaceClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def get_workspace_host():
    spark = SparkSession.builder.getOrCreate()
    workspace_url = spark.conf.get("spark.databricks.workspaceUrl")

    if not workspace_url:
        raise Exception("Unable to retrieve workspace URL from Spark config")

    return f"https://{workspace_url}"


def get_workspace_token():
    spark = SparkSession.builder.getOrCreate()
    dbutils = DBUtils(spark)

    token = dbutils.secrets.get("enforce-scope", "dbx-token")

    if not token:
        raise Exception("Unable to retrieve token from secret scope")

    return token


def enforce():
    host = get_workspace_host()
    token = get_workspace_token()

    w = WorkspaceClient(
        host=host,
        token=token
    )

    endpoints = list(w.serving_endpoints.list())

    logging.info(f"Found {len(endpoints)} endpoints")

    for ep in endpoints:
        logging.info(f"Processing endpoint: {ep.name}")

        try:
            w.serving_endpoints.update_config(
                name=ep.name,
                rate_limits=[{
                    "key": "user",
                    "calls": 0
                }]
            )

            logging.info(f"Rate limit set to 0 for {ep.name}")

        except Exception as e:
            logging.error(f"Failed updating {ep.name}: {str(e)}")
            raise


if __name__ == "__main__":
    enforce()
