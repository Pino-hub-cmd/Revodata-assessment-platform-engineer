import requests
import logging
import os
import json

IMDS_ENDPOINT = "http://169.254.169.254/metadata/identity/oauth2/token"
IMDS_API_VERSION = "2018-02-01"
DATABRICKS_RESOURCE = "https://databricks.azure.net"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def get_workspace_url():
    # Available in Databricks runtime
    return os.environ.get("DATABRICKS_HOST")

def get_managed_identity_token():
    logging.info("Requesting token via Managed Identity")

    params = {
        "api-version": IMDS_API_VERSION,
        "resource": DATABRICKS_RESOURCE
    }

    headers = {
        "Metadata": "true"
    }

    response = requests.get(IMDS_ENDPOINT, params=params, headers=headers, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve token: {response.text}")

    token = response.json().get("access_token")

    if not token:
        raise Exception("Token not found in IMDS response")

    return token

def list_serving_endpoints(host, token):
    url = f"{host}/api/2.0/serving-endpoints"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Failed listing endpoints: {response.text}")

    return response.json().get("endpoints", [])

def set_rate_limit_zero(host, token, endpoint_name):
    url = f"{host}/api/2.0/serving-endpoints/{endpoint_name}/config"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "rate_limits": [
            {
                "key": "user",
                "calls": 0
            }
        ]
    }

    response = requests.patch(url, headers=headers, json=payload, timeout=10)

    if response.status_code not in (200, 201):
        raise Exception(f"Failed updating {endpoint_name}: {response.text}")

def enforce():
    host = get_workspace_url()
    token = get_managed_identity_token()

    endpoints = list_serving_endpoints(host, token)

    updated = 0
    skipped = 0
    failed = 0

    for ep in endpoints:
        name = ep.get("name")

        try:
            config = ep.get("config", {})
            rate_limits = config.get("rate_limits", [])

            already_zero = any(r.get("calls") == 0 for r in rate_limits)

            if already_zero:
                logging.info(f"{name} already compliant")
                skipped += 1
                continue

            set_rate_limit_zero(host, token, name)
            logging.info(f"{name} updated to zero rate limit")
            updated += 1

        except Exception as e:
            logging.error(f"Error processing {name}: {str(e)}")
            failed += 1

    logging.info("===== SUMMARY =====")
    logging.info(f"Updated: {updated}")
    logging.info(f"Skipped: {skipped}")
    logging.info(f"Failed: {failed}")

if __name__ == "__main__":
    enforce()
