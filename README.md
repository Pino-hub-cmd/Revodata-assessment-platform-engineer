# RevoData's Technical Assessment - Platform Engineer

## Introduction

Welcome to the RevoData technical assessment! This project is your opportunity to showcase your expertise in cloud infrastructure, automation, and Databricks platform management.

Imagine yourself as a founding Platform Engineer at a rapidly growing startup. The company has embraced Databricks as its core data platform, but as the number of data scientists and engineers explodes, the environment is becoming chaotic. Your mission is to bring order, security, and automation to the platform, ensuring it can scale efficiently and securely.

### Goal of the Assessment

The primary goal is to demonstrate your ability to provision, configure, and manage a Databricks environment using Infrastructure as Code (IaC) and automation best practices. You will tackle a real-world platform challenge that requires both strategic thinking and hands-on implementation.

## The Challenge: Choose Your Path

We have prepared two distinct challenges. Please choose **one** to complete. Both start with the same foundational step but focus on different aspects of platform engineering.

### Common Prerequisite (For Both Paths)

The solution must include a Databricks workspace on your cloud of choice (Azure or AWS). While you are free to choose and justify any IaC tool, our teams primarily use **Terraform** and **Terragrunt**. Solutions using these tools are therefore strongly preferred.

This assessment is designed to be completed within the limits of trial and the free tier/credits of a new cloud provider account.

---

### Path A: The Guardian of Governance

**Scenario:** The finance department is concerned about the uncontrolled costs associated with experimental Model Serving endpoints. They have mandated that, for the time being, all Model Serving capabilities must be disabled across the workspace to prevent budget overruns.

#### Engineering Deliverables (Path A)

Your task is to build a solution that programmatically disables all existing and future Model Serving endpoints by setting their rate limits to zero.

We recommend organizing your submission with the following structure, using folders only as needed based on your chosen implementation:

-   **Infrastructure as Code** for deploying the Databricks workspace (placed in the `./infra` folder).
-   **Enforcement Logic**: If your solution uses scripts (e.g., Python, Bash), place them in a `./src` folder. If your logic is purely declarative (e.g., entirely within Terraform), it will reside in your `./infra` code.
-   **Tests**: If applicable to your solution, any tests for your core logic should be placed in the `./tests` folder.
-   **Automation Configuration**: Any configuration for running your mechanism, such as Databricks Job definitions or CI/CD pipeline YAMLs (`./.github/workflows` folder).
-   **Documentation**: A detailed `README.md` in the root of the repository. This must justify **why** you chose your particular implementation (e.g., a periodic job vs. a declarative IaC resource vs. another pattern) and discuss its trade-offs.

---

### Path B: The Automation Architect

**Scenario:** To improve cost tracking and accountability, the management team requires that all compute resources be tagged with their respective owner and project. Your task is to enforce this policy automatically, ensuring no untagged clusters can be created.

#### Engineering Deliverables (Path B)

Your task is to implement and enforce a Databricks Cluster Policy that ensures all clusters launched in the workspace have `owner` and `project` tags. The policy should be managed and applied via a CI/CD pipeline.

The following deliverables are expected as part of your project:

- **Infrastructure as Code** for deploying the Databricks workspace (placed in the `./infra` folder).
- **Cluster Policy Definition** as a JSON file (`./resources`).
- **CI/CD Pipeline Definition** (e.g., GitHub Actions workflow YAML) that deploys the cluster policy (stored in `./.github/workflows`).
- **Documentation** for your solution (documented in the `README` and `./docs` folders) - **explain the why, not the how**.
- **Example configurations** or scripts demonstrating the policy in action (e.g., in a `./examples` folder).

---

## General Expectations

Regardless of the path you choose, we are primarily interested in understanding your thought process and engineering practices.

Save everything in a private Git repository and share it with us. Deliver a clean repository: remove any redundant files, replace this README with your own, and provide clear instructions for setting up and running your project. We expect you to spend 3-4 hours on the assessment, so apply your best judgment when prioritizing tasks.

### Stretch Goals

Following are a number of stretch goals of increasing difficulty. We **do not expect** you to achieve all of these. It is better to have a high-quality, complete core assessment than to get lost achieving these goals. Pick what interests you most.

#### Path A Stretch Goals

- **Level 1 / Engineer:**
  - [ ] Build a CI/CD pipeline (e.g., GitHub Actions) that periodically runs your logic to enforce the no-serving-endpoint policy.
- **Level 2 / Future-Proof:**
  - [ ] Implement the solution **without** using a Databricks Personal Access Token (PAT).

#### Path B Stretch Goals

- **Level 1 / Engineer:**
  - [ ] Build a full CI/CD pipeline using GitHub Actions that automatically validates and applies the cluster policy on a push to the `main` branch.
- **Level 2 / Future-Proof:**
  - [ ] Use `pre-commit` hooks to ensure code and configuration quality locally before committing.

### BONUS

- **Level 3 / over 9000 :**
  - [ ] Configure and run your GitHub Actions pipeline on a **self-hosted runner** that you provision in the same cloud environment.

## Review

Once you have completed this project, we will review it together. We will pay special attention to your design choices, automation strategy, and how you addressed potential challenges. We expect issues to arise, so we encourage creative workarounds and proactive measures.

A note on using AI tools (LLMs, coding agents, etc.): we encourage you to use these tools to enhance your productivity. However, please remember that you are 100% responsible for the code you submit. You need to be able to explain how the code works and discuss the pros and cons of your implementations.

Please do **not** use AI assistants in any way during the interview. We want to assess your technical skills, problem-solving abilities, and communication skills on the spot.

**Good luck, and see you on the other side!**
