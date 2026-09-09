# AWS Infrastructure Automation Platform

[![CI](https://github.com/ananyapraneet/aws-infrastructure-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/ananyapraneet/aws-infrastructure-automation/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-oriented AWS infrastructure automation platform that provisions private cloud infrastructure, configures servers, deploys containerized applications, validates infrastructure, and provides **read-only AI-assisted 
infrastructure analysis and troubleshooting**.

Built with **Terraform, Ansible, Docker, Amazon ECR, AWS Systems Manager, Application Load Balancer, Make, Python, Flask, and OpenAI**.

> **Project status:** Complete portfolio project. The AWS environment is designed to be **provisioned on demand for validation and demonstrations**, rather than operated as a permanently running production environment. Validation 
evidence in this repository represents a successfully provisioned and tested environment. The infrastructure can be removed with `make destroy` when no longer required.

---

## Overview

This project demonstrates an end-to-end infrastructure automation workflow covering:

* AWS infrastructure provisioning
* Private VPC networking
* Security group and IAM design
* Private EC2 compute
* Application Load Balancing
* AWS Systems Manager-based server management
* Ansible configuration management
* Docker application deployment
* Private Amazon ECR connectivity
* Immutable container image deployments
* Infrastructure and application validation
* Reproducible operator workflows
* Deterministic infrastructure analysis
* AI-assisted infrastructure explanations
* AI-assisted troubleshooting
* Infrastructure validation
* Continuous integration with GitHub Actions

The platform intentionally avoids public SSH access and does not use a NAT Gateway.

Private EC2 instances are managed through **AWS Systems Manager Session Manager**, while private container images are retrieved through **VPC endpoints**.

The project is designed around a simple lifecycle:

```text
Provision
    ↓
Configure
    ↓
Deploy
    ↓
Validate
    ↓
Analyze
```

Terraform remains the infrastructure source of truth, Ansible handles server configuration and deployment, and the AI layer operates in a **read-only** capacity.

---

# Highlights

### Infrastructure as Code

Terraform provisions the complete AWS environment including:

* VPC
* Public and private subnets
* Route tables
* Security groups
* EC2
* Application Load Balancer
* IAM
* ECR
* SSM endpoints
* ECR endpoints
* S3 gateway endpoint

### Private-by-Design Architecture

The application EC2 instance:

* Has no public IP
* Does not expose SSH
* Runs inside a private subnet
* Is reachable by the ALB only on port `8000`
* Is managed through AWS Systems Manager

### Reproducible Automation

A Makefile provides a simple operator interface:

```bash
make provision
make configure
make deploy
make validate
make plan
make destroy
```

### Immutable Deployments

Application images are tagged using the current Git commit SHA.

```text
Git Commit
    ↓
Short SHA
    ↓
Docker Image
    ↓
Immutable ECR Tag
    ↓
Private EC2
```

### Infrastructure Validation

The validation system checks infrastructure, server configuration, Docker state, deployed image state, and application health.

### Continuous Integration

The repository includes a GitHub Actions CI pipeline that runs automatically on:

* Pushes to `main`
* Pull requests targeting `main`

The pipeline validates both the Python automation/AI code and Terraform configuration.

```text
GitHub Push / Pull Request
            │
            ├───────────────────┐
            ▼                   ▼
     Python Tests        Terraform Validation
            │                   │
            ├── pytest          ├── terraform fmt -check
            │                   ├── terraform init
            │                   └── terraform validate
            │
            └───────────────────┘
                    │
                    ▼
                CI Result
```

The current Python test suite completes with:

```text
22 passed
```

Terraform validation includes formatting checks, initialization without a backend, and configuration validation.

The workflow is defined in:

```text
.github/workflows/ci.yml
```

### AI Infrastructure Copilot

The project includes a read-only AI layer for:

* Infrastructure analysis
* Infrastructure explanations
* Configuration explanations
* Security recommendations
* Deployment troubleshooting
* Failure analysis
* Infrastructure validation

The deterministic analysis layer runs before AI generation so that the AI consumes structured infrastructure findings rather than raw Terraform state.

---

# Architecture

```text
                              Internet
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  Application    │
                         │      Load       │
                         │    Balancer     │
                         │      :80        │
                         └────────┬────────┘
                                  │
                                  │ HTTP :8000
                                  ▼
                    ┌─────────────────────────┐
                    │      Private EC2        │
                    │     Amazon Linux 2023   │
                    │                         │
                    │        Docker           │
                    │           │             │
                    │           ▼             │
                    │    Flask Application    │
                    │        :8000            │
                    └──────────┬──────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ECR Endpoints    SSM Endpoints      S3 Endpoint
              │                │
              ▼                ▼
        Amazon ECR       AWS Systems Manager
                               ▲
                               │
                               │ AWS SSM
                               │
                    ┌──────────┴──────────┐
                    │ Dockerized Ansible  │
                    │      Controller     │
                    └──────────┬──────────┘
                               ▲
                               │
                         Makefile CLI
                               ▲
                               │
                         Developer
```

The architecture separates:

* **Public traffic** through the Application Load Balancer
* **Private application execution** on EC2
* **Private server management** through AWS Systems Manager
* **Private container image access** through VPC endpoints
* **Infrastructure provisioning** through Terraform
* **Configuration management** through Ansible
* **Application deployment** through Docker and ECR
* **Validation** through Ansible
* **Infrastructure analysis** through the AI tooling

---

# Infrastructure Architecture

The AWS environment is deployed in:

```text
Region: ap-south-1
VPC:    10.0.0.0/16
```

Network layout:

```text
VPC 10.0.0.0/16
│
├── Public Subnets
│   ├── 10.0.1.0/24
│   └── 10.0.2.0/24
│       │
│       └── Application Load Balancer
│
└── Private Subnets
    ├── 10.0.11.0/24
    │   │
    │   └── Private EC2
    │
    └── 10.0.12.0/24
```

There is intentionally **no NAT Gateway**.

Private AWS service connectivity is provided through VPC endpoints.

### AWS Resources

| Component          | Configuration             |
| ------------------ | ------------------------- |
| Region             | `ap-south-1`              |
| VPC                | `10.0.0.0/16`             |
| Public Subnet 1    | `10.0.1.0/24`             |
| Public Subnet 2    | `10.0.2.0/24`             |
| Private Subnet 1   | `10.0.11.0/24`            |
| Private Subnet 2   | `10.0.12.0/24`            |
| EC2                | Amazon Linux 2023         |
| EC2 Type           | `t3.micro`                |
| Application Port   | `8000`                    |
| Load Balancer      | Application Load Balancer |
| Load Balancer Port | `80`                      |
| Container Registry | Amazon ECR                |
| Server Management  | AWS Systems Manager       |
| NAT Gateway        | Not used                  |

### VPC Overview

![AWS VPC Overview](docs/screenshots/01-aws-vpc-overview.png)

### Network and Subnets

![AWS Network and Subnets](docs/screenshots/02-network-subnets.png)

---

# Terraform State

The current portfolio implementation uses **local Terraform state**.

Terraform state is stored locally under:

```text
terraform/terraform.tfstate
terraform/terraform.tfstate.backup
```

This is intentional for the scope of this portfolio project and keeps the infrastructure self-contained for demonstration and reproducibility.

However, local state is **not the recommended approach for a production team environment**.

A production implementation should use a remote Terraform backend with appropriate access control and state concurrency protection.

A typical production architecture would look like:

```text
Terraform
    │
    ▼
Remote State Backend
    │
    ├── Shared state
    ├── Controlled access
    └── State locking / concurrency protection
```

A future production deployment could use an Amazon S3-backed Terraform state architecture with appropriate locking and access controls.

Therefore, remote Terraform state is a documented production consideration rather than a capability currently implemented by this repository.

---

# Private EC2 and SSM Management

The EC2 instance is intentionally private.

It does not require:

* A public IPv4 address
* Internet-facing SSH
* A bastion host
* SSH key distribution

Instead, the management path is:

```text
Developer
    │
    ▼
Dockerized Ansible Controller
    │
    │ AWS SSM
    ▼
SSM VPC Endpoints
    │
    ▼
Private EC2
```

The EC2 IAM role includes:

```text
AmazonSSMManagedInstanceCore
```

This allows Systems Manager to manage the instance without exposing SSH.

### Private EC2 / SSM Evidence

![Private EC2 and SSM](docs/screenshots/03-private-ec2-ssm.png)

---

# Application Load Balancer

The Application Load Balancer provides the public entry point to the application.

```text
Internet
   │
   ▼
ALB :80
   │
   │ HTTP :8000
   ▼
Private EC2
   │
   ▼
Docker Container
   │
   ▼
Flask :8000
```

The EC2 security group does not allow unrestricted application access.

Application traffic is permitted only from the ALB security group.

### Load Balancer

![Application Load Balancer](docs/screenshots/04-alb.png)

### Application Health

The application exposes:

```text
GET /
GET /health
```

The health endpoint returns:

```json
{
  "status": "healthy"
}
```

The ALB health endpoint was successfully validated externally.

![ALB Health Check](docs/screenshots/06-alb-health.png)

---

# Security Group Design

Security groups are separated by responsibility.

```text
Internet
   │
   ▼
ALB Security Group
   │
   │ TCP 8000
   ▼
EC2 Security Group
```

The EC2 security group:

* Allows application traffic from the ALB security group
* Does not expose SSH to the internet
* Does not allow unrestricted application access

The ALB is the public-facing component; the application server remains private.

![Security Group Configuration](docs/screenshots/05-security-groups.png)

---

# Private Container Image Connectivity

The EC2 instance does not require public internet access to retrieve its application image.

Private connectivity is provided through:

* ECR API interface endpoint
* ECR Docker Registry interface endpoint
* S3 gateway endpoint

The connectivity model is:

```text
Private EC2
     │
     ├── ECR API Endpoint
     │
     ├── ECR DKR Endpoint
     │
     └── S3 Gateway Endpoint
             │
             ▼
          Amazon ECR
```

This allows the application server to pull images from ECR without requiring a NAT Gateway.

---

# Docker Application

The application is a lightweight Flask service.

```text
Flask
  │
  ▼
Docker
  │
  ▼
Port 8000
```

Endpoints:

```text
GET /
GET /health
```

Example root response:

```json
{
  "service": "aws-infrastructure-automation",
  "status": "running"
}
```

Example health response:

```json
{
  "status": "healthy"
}
```

The application container:

* Uses Python 3.12
* Runs as a non-root user
* Exposes port `8000`
* Includes a Docker health check
* Is deployed through Ansible

---

# Git-Based Deployment

Application images are tagged using the current Git commit SHA.

The Makefile derives the tag with:

```makefile
IMAGE_TAG ?= $(shell git rev-parse --short HEAD)
```

For example:

```text
6f7197d
```

The resulting image becomes:

```text
aws-infrastructure-app:6f7197d
```

The image is pushed to Amazon ECR using the same immutable tag.

The deployment chain is therefore:

```text
Git Commit
    ↓
Short Commit SHA
    ↓
Docker Build
    ↓
Amazon ECR
    ↓
Private EC2
    ↓
Running Container
```

ECR uses **immutable image tags**, preventing an existing image tag from being overwritten.

This provides deployment traceability from source code to the running application.

---

# Deployment Flow

The complete deployment workflow is:

```text
Git Commit SHA
      │
      ▼
Docker Build
      │
      ▼
ECR Authentication
      │
      ▼
Immutable ECR Tag
      │
      ▼
Push Image
      │
      ▼
Ansible via SSM
      │
      ▼
Private EC2
      │
      ▼
Docker Pull
      │
      ▼
Container Replacement
      │
      ▼
Running Application
```

Terraform manages infrastructure.

Docker and ECR manage application images.

Ansible manages application deployment.

AWS Systems Manager provides the private management path.

---

# Reproducible Automation

The Makefile provides a simplified operator interface over the infrastructure lifecycle.

```bash
make provision
make configure
make deploy
make validate
make plan
make destroy
```

## Command Responsibilities

| Command          | Responsibility                                |
| ---------------- | --------------------------------------------- |
| `make provision` | Provision AWS infrastructure with Terraform   |
| `make plan`      | Preview Terraform infrastructure changes      |
| `make configure` | Configure private EC2 with Ansible            |
| `make deploy`    | Build, tag, push, and deploy the application  |
| `make validate`  | Validate infrastructure and application state |
| `make destroy`   | Destroy provisioned AWS infrastructure        |

The lifecycle remains intentionally separated:

```text
Provision
    ↓
Configure
    ↓
Deploy
    ↓
Validate
```

This makes each stage independently executable and easier to troubleshoot.

---

# Ansible Configuration

The Ansible playbook separates configuration, deployment, and validation through tags.

```yaml
---
- name: Configure application servers
  hosts: app_servers
  become: true

  roles:
    - { role: user_setup, tags: [configure] }
    - { role: ssh_hardening, tags: [configure] }
    - { role: system_config, tags: [configure] }
    - { role: docker, tags: [configure] }
    - { role: security_hardening, tags: [configure] }
    - { role: application, tags: [deploy] }
    - { role: validation, tags: [validate] }
```

The lifecycle can therefore be executed independently:

```bash
ansible-playbook \
  -i inventory/hosts.yml \
  site.yml \
  --tags configure
```

```bash
ansible-playbook \
  -i inventory/hosts.yml \
  site.yml \
  --tags deploy
```

```bash
ansible-playbook \
  -i inventory/hosts.yml \
  site.yml \
  --tags validate
```

The Makefile provides the corresponding simplified commands:

```bash
make configure
make deploy
make validate
```

---

# Dockerized Ansible Controller

The Ansible execution environment is itself containerized.

```text
Developer Machine
       │
       ▼
Docker
       │
       ▼
Ansible Controller
       │
       ├── Ansible Core
       ├── AWS CLI
       ├── Boto3
       ├── Session Manager Plugin
       └── Required Ansible Collections
       │
       ▼
AWS Systems Manager
```

The controller image is:

```text
aws-infra-ansible
```

Containerizing the controller provides:

* Reproducible Ansible execution
* Host Python isolation
* Consistent dependencies
* Linux-based execution behavior
* Portable automation
* Reliable Ansible-over-SSM execution

---

# Infrastructure Validation

The validation layer verifies both infrastructure and application state.

Checks include:

* Operating system
* Docker service state
* Docker service enabled state
* IPv4 forwarding
* Application port availability
* Application container existence
* Application container running state
* Container restart policy
* Expected ECR image tag
* Docker health status
* Local `/health` endpoint
* Deployed image existence
* Running container image
* Running container image matching the deployed image
* Application Load Balancer `/health` endpoint

The final validation run completed successfully:

```text
PLAY RECAP

app : ok=22 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

### Deployment Validation Evidence

![Deployment Validation](docs/screenshots/07-deployment-validation.png)

---

# Continuous Integration

The repository uses GitHub Actions to automatically validate changes.

The CI workflow runs on:

* Pushes to `main`
* Pull requests targeting `main`

The pipeline contains two independent validation jobs.

### Python Tests

The Python job:

1. Checks out the repository
2. Sets up Python 3.12
3. Installs project dependencies
4. Runs `pytest`

Current result:

```text
22 passed
```

### Terraform Validation

The Terraform job:

1. Checks out the repository
2. Sets up Terraform
3. Runs recursive formatting checks
4. Initializes Terraform with the backend disabled
5. Runs `terraform validate`

The workflow intentionally uses:

```bash
terraform init -backend=false
```

because the current portfolio implementation uses local Terraform state and CI does not need to access or modify deployed infrastructure.

The complete CI flow is:

```text
Pull Request / Push
        │
        ├───────────────────────┐
        ▼                       ▼
 Python Tests             Terraform Validation
        │                       │
        ▼                       ├── fmt -check
     pytest                    ├── init
        │                       └── validate
        │
        └───────────┬───────────┘
                    ▼
               CI Success
```

The workflow is located at:

```text
.github/workflows/ci.yml
```

---

# AI Infrastructure Copilot

The project includes a read-only **AI Infrastructure Copilot**.

The AI layer does not provision infrastructure, execute commands, or directly modify AWS resources.

Its purpose is to help an operator understand infrastructure and diagnose issues while keeping infrastructure changes under explicit human control.

The architecture is:

```text
                    infra-ai
                       │
                       ▼
                Terraform JSON
                       │
                       ▼
          Deterministic Infrastructure
                 Analyzer
                       │
                       ▼
                    Findings
                       │
                       ▼
              AI Explanation Layer
                       │
                       ▼
        Human-readable Recommendations
```

The important design principle is:

```text
Terraform State
      ↓
Deterministic Analysis
      ↓
Structured Findings
      ↓
AI Interpretation
      ↓
Human Decision
```

The AI does not become the source of truth.

Terraform remains the source of truth for infrastructure.

---

# AI CLI

The project provides the following commands:

```bash
infra-ai analyze
infra-ai explain <file>
infra-ai troubleshoot <file>
infra-ai validate
```

## AI CLI Setup

The AI CLI is installed as an editable local Python package.

From the repository root:

```bash
pip install -e .
```

This installs the `infra-ai` command and allows the CLI to be used directly from the development environment.

### OpenAI Configuration

The OpenAI integration reads the `OPENAI_API_KEY` environment variable.

Export the key before using AI-powered commands:

```bash
export OPENAI_API_KEY="your-api-key"
```

For local development, the value can also be stored in a `.env` file:

```text
OPENAI_API_KEY=your-api-key
```

If using a `.env` file, load/export the variable through the developer's preferred environment-loading mechanism before running the AI-powered CLI commands.

The `.env` file must remain local and must **never be committed to Git**.

The deterministic infrastructure analysis and validation commands do not require an OpenAI API key.

Verify that the CLI is installed:

```bash
infra-ai --help
```

The AI layer remains read-only:

```text
Terraform / Input
       ↓
Deterministic Analysis
       ↓
Structured Findings
       ↓
OpenAI Explanation
       ↓
Human Review
```

No infrastructure changes are automatically executed by the AI layer.

---

## `infra-ai analyze`

Analyzes Terraform infrastructure using deterministic analysis.

The analyzer loads Terraform state through:

```text
terraform show -json
```

and extracts infrastructure resources for analysis.

The current infrastructure contains:

```text
38 resources
```

The analyzer checks areas including:

### Security

* Public SSH access
* Public application access

### IAM

* Systems Manager permissions
* ECR read permissions

### Network

* ECR API endpoint
* ECR Docker Registry endpoint
* SSM endpoint
* SSMMessages endpoint
* S3 endpoint

The current production infrastructure produces:

```text
Resources analyzed: 38
Findings: 0
```

### Infrastructure Analysis Evidence

![AI Infrastructure Analysis](docs/screenshots/08-ai-infrastructure-analysis.png)

---

# Deterministic Analysis

The AI layer is intentionally placed **after deterministic infrastructure analysis**.

For example, a controlled insecure security group test produces:

```text
Severity: HIGH
Category: SECURITY
Resource: test.security_group.insecure

Title:
SSH exposed to the internet

Recommendation:
Restrict SSH access to a trusted CIDR or use AWS Systems Manager.
```

This approach provides several advantages:

* Predictable infrastructure checks
* Testable findings
* Reduced hallucination risk
* Structured AI input
* Separation between detection and explanation

The AI receives structured findings rather than having to infer the infrastructure state from raw Terraform data.

---

# AI Explain

The `infra-ai explain` command accepts a file as its source of truth.

```bash
infra-ai explain <file>
```

The explanation layer is designed to:

* Explain observed infrastructure or configuration
* Use only the supplied file contents as evidence
* Distinguish observed configuration from recommendations
* Avoid inventing infrastructure
* Avoid executing commands
* Avoid automatically changing infrastructure

This makes the explanation layer suitable for reviewing configuration files, infrastructure artifacts, and operational outputs.

---

# AI Troubleshooting

The `infra-ai troubleshoot` command analyzes an operational failure or diagnostic file.

```bash
infra-ai troubleshoot <file>
```

The troubleshooting workflow is designed to identify:

1. Most likely cause
2. Evidence supporting the diagnosis
3. Other plausible causes when evidence is insufficient
4. Practical validation checks
5. Recommended resolution

The troubleshooting system explicitly distinguishes:

```text
Evidence
   ↓
Inference
   ↓
Recommendation
```

It does not assume access to systems or infrastructure that are not represented in the supplied input.

It also does not execute commands or automatically modify infrastructure.

A synthetic deployment failure fixture is included in the repository for testing the troubleshooting logic.

---

# Infrastructure Validation CLI

The `infra-ai validate` command provides deterministic infrastructure validation.

```bash
infra-ai validate
```

Current validation result:

```text
Infrastructure Validation
-------------------------

Resources validated: 38
Checks performed: 4
Findings: 0

Validation: PASSED
No infrastructure validation issues detected.
```

This provides a second validation interface alongside the Ansible deployment validation.

---

# Validation Evidence

The project includes multiple layers of validation.

### Ansible Validation

```text
app : ok=22 changed=0 unreachable=0 failed=0
```

### Infrastructure Validation

```text
Resources validated: 38
Checks performed: 4
Findings: 0

Validation: PASSED
```

### Automated Tests

```text
22 passed
```

### External Application Validation

The Application Load Balancer successfully returned:

```json
{
  "status": "healthy"
}
```

### Validation and Test Evidence

![Validation and Tests](docs/screenshots/09-validation-and-tests.png)

### Continuous Integration

GitHub Actions validates the repository on pushes to `main` and pull requests.

The CI pipeline performs:

```text
Python Tests
    ↓
pytest
    ↓
Terraform Formatting
    ↓
terraform fmt -check
    ↓
Terraform Initialization
    ↓
terraform init -backend=false
    ↓
Terraform Validation
    ↓
terraform validate
```

Current CI validation:

```text
Python Tests
22 passed

Terraform
Formatting: PASSED
Initialization: PASSED
Validation: PASSED
```

The CI workflow is defined in:

```text
.github/workflows/ci.yml
```

This provides automated regression and infrastructure configuration checks alongside the project's deployment validation.

---

# Test Coverage

The AI and infrastructure automation components include automated tests covering:

```text
tests/
├── ai/
│   ├── test_openai.py
│   ├── test_prompts.py
│   └── test_reporting.py
│
├── cli/
│   ├── test_explain.py
│   └── test_troubleshoot.py
│
├── explain/
│   └── test_explainer.py
│
├── inputs/
│   └── test_files.py
│
├── troubleshoot/
│   └── test_troubleshooter.py
│
├── validation/
│   └── test_validator.py
│
└── fixtures/
    └── deployment-error.txt
```

The final test suite completed with:

```text
22 passed
```

The OpenAI provider tests use mocked API calls and isolated test credentials, so the test suite does not require a real OpenAI API key or external API access.

---

# Repository Structure

```text
aws-infrastructure-automation/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── ansible/
│   ├── Dockerfile
│   ├── ansible.cfg
│   ├── inventory/
│   │   └── hosts.yml
│   ├── site.yml
│   └── roles/
│       ├── user_setup/
│       ├── ssh_hardening/
│       ├── system_config/
│       ├── docker/
│       ├── security_hardening/
│       ├── application/
│       └── validation/
│
├── infra_ai/
│   ├── ai/
│   │   ├── base.py
│   │   ├── openai.py
│   │   └── prompts.py
│   │
│   ├── analyzer/
│   │   ├── analyzer.py
│   │   ├── iam.py
│   │   ├── network.py
│   │   ├── security.py
│   │   ├── terraform.py
│   │   └── test_data.py
│   │
│   ├── cli/
│   │   └── main.py
│   │
│   ├── explain/
│   │   └── explainer.py
│   │
│   ├── inputs/
│   │   └── files.py
│   │
│   ├── reporting/
│   │   └── report.py
│   │
│   ├── troubleshoot/
│   │   └── troubleshooter.py
│   │
│   └── validation/
│       └── validator.py
│
├── terraform/
│   ├── .terraform.lock.hcl
│   ├── alb.tf
│   ├── ansible_ssm.tf
│   ├── ec2.tf
│   ├── ecr.tf
│   ├── ecr_endpoints.tf
│   ├── iam.tf
│   ├── main.tf
│   ├── outputs.tf
│   ├── providers.tf
│   ├── routes.tf
│   ├── s3_endpoint.tf
│   ├── security_groups.tf
│   ├── ssm.tf
│   ├── subnets.tf
│   ├── terraform.tfstate
│   ├── terraform.tfstate.backup
│   ├── variables.tf
│   ├── versions.tf
│   └── vpc.tf
│
├── tests/
│   ├── ai/
│   ├── cli/
│   ├── explain/
│   ├── fixtures/
│   ├── inputs/
│   ├── troubleshoot/
│   └── validation/
│
├── docs/
│   └── screenshots/
│       ├── 01-aws-vpc-overview.png
│       ├── 02-network-subnets.png
│       ├── 03-private-ec2-ssm.png
│       ├── 04-alb.png
│       ├── 05-security-groups.png
│       ├── 06-alb-health.png
│       ├── 07-deployment-validation.png
│       ├── 08-ai-infrastructure-analysis.png
│       └── 09-validation-and-tests.png
│
├── Makefile
├── .gitignore
└── README.md
```

---

# Technology Stack

## Infrastructure

* AWS
* Terraform
* VPC
* EC2
* Application Load Balancer
* IAM
* Amazon ECR
* AWS Systems Manager
* VPC Endpoints

## Configuration Management

* Ansible
* AWS SSM connection plugin
* Dockerized Ansible controller
* Ansible Collections

## Application

* Python
* Flask
* Docker

## Automation

* Make
* Git
* Bash
* GitHub Actions

## AI

* Python
* OpenAI API
* Deterministic infrastructure analysis
* AI-assisted explanations
* AI-assisted troubleshooting
* Infrastructure validation

---

# Security Considerations

Security was considered throughout the infrastructure design rather than added as a final layer.

## No Public EC2 Access

The EC2 instance does not expose SSH to the internet.

## Private Server Management

AWS Systems Manager is used instead of public SSH.

## Private Application Server

The application runs on a private EC2 instance.

## Security Group Separation

The ALB and EC2 use separate security groups.

The EC2 security group accepts application traffic only from the ALB security group.

## Non-Root Container

The application container runs as a non-root user.

## Immutable ECR Tags

ECR image tags are configured as immutable.

## ECR Image Scanning

ECR scan-on-push is enabled.

## IAM Permissions

The EC2 instance is assigned permissions required for:

* Systems Manager management
* ECR image retrieval

## Read-Only AI

The AI layer cannot directly modify AWS infrastructure.

Its responsibility is limited to:

```text
Analyze
Explain
Recommend
Troubleshoot
Validate
```

Infrastructure changes remain an explicit operator responsibility.

---

# Cost Considerations

The architecture is designed to balance private connectivity, security, and cost awareness while remaining realistic for a portfolio environment.

The design intentionally avoids:

* NAT Gateway
* Bastion host
* Public EC2 management
* Unnecessary managed services

Private AWS service connectivity is instead provided through VPC endpoints.

### NAT Gateway vs VPC Endpoints

Avoiding a NAT Gateway does **not** mean that VPC endpoints are free.

NAT Gateways can incur:

* Hourly charges
* Data-processing charges

VPC interface endpoints can also incur:

* Hourly endpoint charges
* Data-processing charges depending on usage

The architectural decision in this project is therefore not based on the assumption that VPC endpoints are universally cheaper.

Instead, the design uses VPC endpoints because the private EC2 instance only requires access to a defined set of AWS services:

```text
Private EC2
     │
     ├── ECR API
     ├── ECR DKR
     ├── SSM
     ├── SSMMessages
     └── S3
```

This avoids routing general private-subnet traffic through a NAT Gateway and provides private connectivity to the AWS services required by the workload.

For a small portfolio environment, the resulting architecture demonstrates an important real-world trade-off:

```text
Private Connectivity
        +
Security
        +
Controlled AWS Service Access
        +
Cost Awareness
```

Actual AWS costs depend on region, endpoint count, availability-zone placement, traffic volume, storage, and usage patterns.

The environment is therefore intended to be **provisioned when needed and destroyed when no longer required**.

---

# Host Prerequisites

The operator machine requires:

* Docker
* AWS CLI
* Terraform
* Make
* Git
* Python 3.12+

AWS credentials must also be configured.

The current Makefile defaults to:

```text
AWS_PROFILE=admin-1
AWS_REGION=ap-south-1
```

The Dockerized Ansible controller image must be available locally:

```text
aws-infra-ansible
```

The Python environment used for the AI CLI should have the project installed in editable mode:

```bash
pip install -e .
```

Docker and AWS CLI remain host prerequisites because they are used for operations such as:

* Building the application image
* Authenticating to ECR
* Pushing the application image
* Running the Ansible controller

---

# Deployment

## 1. Configure AWS

Configure an AWS CLI profile with permissions to provision the required infrastructure.

The project currently uses:

```text
AWS_PROFILE=admin-1
AWS_REGION=ap-south-1
```

These values can be overridden:

```bash
AWS_PROFILE=<profile> AWS_REGION=<region> make provision
```

---

## 2. Install the AI CLI

Create or activate the Python environment used for the project and install the repository:

```bash
pip install -e .
```

This installs the `infra-ai` command.

For AI-powered functionality, configure the OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

The key is used only by the AI explanation layer and should never be committed to the repository.

The deterministic infrastructure analysis and validation commands can be used without an OpenAI API key.

---

## 3. Provision Infrastructure

Initialize and apply Terraform:

```bash
make provision
```

Or preview changes first:

```bash
make plan
```

Terraform provisions the AWS networking, security, compute, load balancing, IAM, ECR, SSM, and private connectivity components.

---

## 4. Configure the Server

Run the Ansible configuration workflow:

```bash
make configure
```

This configures the private EC2 instance through AWS Systems Manager.

---

## 5. Deploy the Application

Build and deploy the application:

```bash
make deploy
```

The workflow performs:

```text
Docker Build
    ↓
ECR Login
    ↓
Git SHA Tag
    ↓
ECR Push
    ↓
Ansible Deployment
    ↓
AWS SSM
    ↓
Private EC2
```

---

## 6. Validate

Run:

```bash
make validate
```

The validation workflow checks the server, Docker, deployed image, container health, application endpoint, and ALB health.

---

## 7. Analyze Infrastructure

Run the infrastructure analyzer:

```bash
infra-ai analyze
```

Expected healthy infrastructure result:

```text
Resources analyzed: 38
Findings: 0
```

---

## 8. Validate Infrastructure with the AI CLI

Run:

```bash
infra-ai validate
```

Expected result:

```text
Infrastructure Validation
-------------------------

Resources validated: 38
Checks performed: 4
Findings: 0

Validation: PASSED
```

---

# Cleanup

When the environment is no longer required, destroy the provisioned AWS resources:

```bash
make destroy
```

This executes:

```text
terraform destroy
```

Before destroying an environment, ensure that any resources or data that need to be retained have been backed up.

Because this project is designed for on-demand portfolio demonstrations, destroying the environment after validation is the expected operating pattern when the infrastructure is not actively being demonstrated.

---

# Failure Scenarios and Troubleshooting

The project includes a synthetic deployment failure fixture:

```text
tests/fixtures/deployment-error.txt
```

The fixture represents an application deployment failure involving an ECR authentication problem.

The troubleshooting CLI can analyze the fixture with:

```bash
infra-ai troubleshoot tests/fixtures/deployment-error.txt
```

The purpose of the fixture is to test the troubleshooting workflow without requiring a live infrastructure failure.

The troubleshooting design emphasizes:

```text
Observed Evidence
        ↓
Likely Cause
        ↓
Additional Possibilities
        ↓
Validation Checks
        ↓
Recommended Resolution
```

The system does not automatically modify infrastructure based on its diagnosis.

---

# Key Design Decisions

## Why private EC2?

The application server does not need to be directly accessible from the internet.

The ALB provides the public application entry point while EC2 remains private.

## Why AWS Systems Manager instead of SSH?

SSM removes the need for:

* Public IP addresses
* Public SSH
* Bastion infrastructure
* SSH key distribution

This significantly reduces the attack surface of the management plane.

## Why no NAT Gateway?

The application server only needs private access to a defined set of AWS services.

VPC endpoints provide private connectivity to those services without requiring the private subnet to route through a NAT Gateway.

This is not assumed to be universally cheaper than VPC endpoints. Both architectures have associated costs.

The decision is primarily based on:

* Reducing unnecessary internet egress paths
* Providing private AWS service connectivity
* Avoiding NAT Gateway hourly and data-processing charges
* Limiting private-subnet connectivity to required AWS services
* Keeping the portfolio architecture cost-aware

For a small workload, endpoint costs and NAT Gateway costs should be evaluated against the actual number of endpoints, availability zones, and traffic volume.

## Why immutable ECR tags?

Git commit SHA-based immutable tags create a direct relationship between:

```text
Source Code
    ↓
Git Commit
    ↓
Docker Image
    ↓
ECR
    ↓
Deployment
```

This improves deployment traceability and prevents accidental tag reuse.

## Why deterministic analysis before AI?

AI is useful for explanation and reasoning, but infrastructure policy checks should be deterministic wherever possible.

Therefore:

```text
Infrastructure
      ↓
Deterministic Checks
      ↓
Structured Findings
      ↓
AI Explanation
```

This reduces ambiguity and makes the core security checks testable.

## Why read-only AI?

An AI system should not directly mutate production infrastructure based on generated output.

The project therefore deliberately separates:

```text
AI Recommendation
        ≠
Infrastructure Change
```

The human operator remains responsible for reviewing and applying changes.

## Why local Terraform state?

The current implementation uses local Terraform state to keep the portfolio project self-contained.

This simplifies demonstration and avoids introducing additional backend infrastructure into the project.

However, local state is not appropriate for collaborative production infrastructure.

A production implementation should use a remote backend with controlled access and state concurrency protection.

---

# Portfolio Projects

This project is part of a broader GitHub portfolio demonstrating application development, CI/CD, infrastructure automation, and cloud engineering.

| Project                                                | Focus                                                                                                    | Repository                                                                                               
|
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- | 
-------------------------------------------------------------------------------------------------------- |
| **Project 1 — Bookify API**                            | Production-ready SaaS backend with authentication, PostgreSQL, Redis, Celery, Docker, and AWS deployment | [Bookify API](https://github.com/ananyapraneet/bookify-api)                                              
|
| **Project 2 — CI/CD Platform**                         | Complete CI/CD platform using Docker, GitHub Actions, automated testing, and deployment workflows        | [CI/CD Platform](https://github.com/ananyapraneet/cicd-platform)                                         
|
| **Project 3 — AWS Infrastructure Automation Platform** | Terraform, Ansible, AWS, private EC2, ECR, SSM, validation, and AI-assisted infrastructure analysis      | [AWS Infrastructure Automation 
Platform](https://github.com/ananyapraneet/aws-infrastructure-automation) |

Together, the three projects demonstrate an increasingly complete engineering lifecycle:

```text
Application
    ↓
CI/CD
    ↓
Infrastructure Automation
    ↓
Cloud Deployment
    ↓
Validation
    ↓
AI-Assisted Operations
```

---

# Development Stages

The project was developed incrementally to demonstrate the evolution from basic infrastructure provisioning to a complete automation and analysis platform.

```text
Stage 1
Project Initialization
        ↓
Stage 2
Terraform Foundation
        ↓
Stage 3
AWS Networking
        ↓
Stage 4
Security & IAM
        ↓
Stage 5
EC2 + ALB + Private SSM + Private Connectivity
        ↓
Stage 6
Ansible Configuration
        ↓
Stage 7
Docker Application Deployment
        ↓
Stage 8
Monitoring & Validation
        ↓
Stage 9
Reproducible Automation
        ↓
Stage 10
AI Infrastructure Copilot
        ↓
Stage 11
AI Explain & Failure Analysis
        ↓
Stage 12
Portfolio & Documentation
```

---

# Project Status

| Area                           | Status             |
| ------------------------------ | ------------------ |
| Terraform Infrastructure       | ✅ Complete         |
| Terraform CI Validation        | ✅ Complete         |
| VPC Networking                 | ✅ Complete         |
| Security Groups                | ✅ Complete         |
| IAM                            | ✅ Complete         |
| Private EC2                    | ✅ Complete         |
| Application Load Balancer      | ✅ Complete         |
| AWS Systems Manager            | ✅ Complete         |
| Private ECR Connectivity       | ✅ Complete         |
| Ansible Configuration          | ✅ Complete         |
| Docker Application Deployment  | ✅ Complete         |
| Infrastructure Validation      | ✅ Complete         |
| Reproducible Makefile Workflow | ✅ Complete         |
| AI Infrastructure Analysis     | ✅ Complete         |
| AI Infrastructure Explanation  | ✅ Complete         |
| AI Troubleshooting             | ✅ Complete         |
| AI Infrastructure Validation   | ✅ Complete         |
| GitHub Actions CI              | ✅ Complete         |
| Portfolio Documentation        | ✅ Complete         |
| Remote Terraform State Backend | ⚠️ Not Implemented |

The AWS environment itself is **not intended to remain permanently active**. It is provisioned on demand for demonstrations and validation and can be removed with:

```bash
make destroy
```

---

# Final Validation

The completed platform has been validated across the major layers:

```text
Terraform
   │
   ▼
AWS Infrastructure
   │
   ▼
Ansible Configuration
   │
   ▼
Docker Deployment
   │
   ▼
Private EC2
   │
   ▼
Application Load Balancer
   │
   ▼
/health → 200 OK
```

And the infrastructure analysis path:

```text
Terraform State
      │
      ▼
Deterministic Analyzer
      │
      ▼
38 Resources
      │
      ▼
0 Findings
      │
      ▼
Validation Passed
```

Automated tests completed successfully:

```text
22 passed
```

Ansible validation completed successfully:

```text
app : ok=22 changed=0 unreachable=0 failed=0
```

GitHub Actions CI completed successfully with:

```text
Python Tests
22 passed

Terraform Formatting
PASSED

Terraform Initialization
PASSED

Terraform Validation
PASSED
```

The platform therefore demonstrates a complete infrastructure lifecycle from **provisioning to deployment, validation, continuous integration, and AI-assisted analysis**.

---

# License

This project is licensed under the MIT License.

See [LICENSE](LICENSE) for details.

