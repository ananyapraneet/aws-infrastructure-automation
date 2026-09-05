# AWS Infrastructure Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Reproducible AWS infrastructure provisioning and server configuration using **Terraform, Ansible, Docker, and AI-assisted infrastructure analysis**.

## Overview

**AWS Infrastructure Automation** is a DevOps/SRE-focused infrastructure automation platform designed to provision, configure, deploy, and validate a complete application environment on AWS.

The project combines:

* **Terraform** for infrastructure provisioning
* **Ansible** for server configuration and configuration management
* **Docker** for application deployment
* **AWS** for cloud infrastructure
* **AI Infrastructure Copilot** for infrastructure analysis, security recommendations, configuration explanations, and failure analysis

The primary goal is to make the infrastructure **reproducible, automated, explainable, secure, and cost-conscious**.

---

## Architecture

The target architecture follows a clear separation of responsibilities:

```text
                         Internet
                            │
                            ▼
                 ┌────────────────────┐
                 │ Application Load   │
                 │      Balancer      │
                 └─────────┬──────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │           AWS VPC        │
              │                          │
              │  ┌────────────────────┐  │
              │  │   Public Subnets   │  │
              │  │                    │  │
              │  │       ALB          │  │
              │  └────────┬───────────┘  │
              │           │              │
              │  ┌────────▼───────────┐  │
              │  │  Private Subnets   │  │
              │  │                    │  │
              │  │       EC2          │  │
              │  │        │           │  │
              │  │      Docker        │  │
              │  │        │           │  │
              │  │   Application      │  │
              │  └────────────────────┘  │
              └──────────────────────────┘


       Terraform
           │
           │ Provision
           ▼
      AWS Infrastructure
           │
           │ Configure
           ▼
        Ansible
           │
           │ Deploy
           ▼
         Docker
           │
           ▼
      Application


    Terraform Plan
           │
           ▼
   AI Infrastructure
       Copilot
           │
     ┌─────┼─────────────┐
     ▼     ▼             ▼
 Security  Config.     Failure
 Analysis  Analysis     Analysis
```

The architecture is being implemented incrementally.

**Current implementation:** the AWS networking foundation is complete, including the VPC, public and private subnets, routing, Internet Gateway, and security groups.

**Planned implementation:** EC2, IAM, private server management, Application Load Balancer, Docker deployment, monitoring, and AI-assisted infrastructure analysis will be added in subsequent stages.

Terraform and Ansible remain responsible for making infrastructure and configuration changes.

The AI layer is intentionally **read-only with respect to infrastructure changes**: it analyzes and recommends but does not directly modify AWS resources.

---

## Core Workflow

The target deployment workflow is:

```text
Terraform
    │
    ▼
Provision AWS infrastructure
    │
    ├── VPC
    ├── Public / Private Subnets
    ├── Route Tables
    ├── Security Groups
    ├── IAM Roles
    ├── EC2
    └── Load Balancer
    │
    ▼
Ansible
    │
    ├── Configure users
    ├── Configure private server access
    ├── Install Docker
    ├── Configure server
    ├── Configure monitoring
    └── Validate server
    │
    ▼
Docker
    │
    ▼
Deploy Application
    │
    ▼
Post-Deployment Validation
    │
    ▼
Running Application
```

The final project will provide a simplified interface for executing these workflows.

Example:

```bash
make provision
make configure
make deploy
make validate
```

---

## AI Infrastructure Copilot

The project will include an **AI Infrastructure Copilot** that provides an intelligence layer around the infrastructure automation workflow.

Example:

```text
Terraform
    │
    ▼
Terraform Plan
    │
    ▼
Infrastructure Analysis
    │
    ▼
AI Infrastructure Copilot
    │
    ├── Security Risks
    ├── Configuration Issues
    ├── Potential Failures
    ├── Infrastructure Explanation
    ├── Remediation Suggestions
    └── Cost-Awareness Recommendations
```

Example analysis:

```text
⚠ SECURITY RISK

SSH access is exposed to 0.0.0.0/0.

Recommendation:
Restrict SSH access to a trusted CIDR range
or use a managed access mechanism.
```

Another example:

```text
⚠ MONITORING

The EC2 instance does not appear to have
the expected monitoring permissions.

Recommendation:
Review the instance IAM role and attach
only the required monitoring permissions.
```

The AI component is designed to **recommend and explain**, while Terraform and Ansible remain responsible for actual infrastructure changes.

### Planned CLI

```bash
infra-ai analyze
infra-ai explain
infra-ai validate
infra-ai troubleshoot
```

The AI layer will be designed to support **local, zero-cost execution** where practical. Paid LLM APIs are not required for the core project.

---

## Technology Stack

| Category                 | Technology             |
| ------------------------ | ---------------------- |
| Cloud                    | AWS                    |
| Infrastructure as Code   | Terraform              |
| Configuration Management | Ansible                |
| Containerization         | Docker                 |
| Application              | Python                 |
| Infrastructure AI        | Local LLM / AI tooling |
| Automation               | Make                   |
| Version Control          | Git / GitHub           |
| Operating System         | Linux                  |

---

## Project Structure

The repository is organized around clear infrastructure and automation responsibilities:

```text
aws-infrastructure-automation/
│
├── terraform/
│   ├── providers.tf
│   ├── versions.tf
│   ├── variables.tf
│   ├── main.tf
│   ├── outputs.tf
│   ├── vpc.tf
│   ├── subnets.tf
│   ├── routes.tf
│   └── security_groups.tf
│
├── ansible/
│   └── Server configuration and deployment
│
├── app/
│   └── Containerized application
│
├── infra-ai/
│   └── AI Infrastructure Copilot
│
├── scripts/
│   └── Supporting automation scripts
│
├── Makefile
├── README.md
├── LICENSE
└── .gitignore
```

The directory structure will evolve as each implementation stage is completed.

---

## Infrastructure Components

The target AWS environment will include:

### Implemented

* VPC
* Public subnets
* Private subnets
* Route tables
* Internet Gateway
* Security groups

The current networking foundation uses:

```text
VPC
10.0.0.0/16
│
├── Public Subnet A
│   └── 10.0.1.0/24
│
├── Public Subnet B
│   └── 10.0.2.0/24
│
├── Private Subnet A
│   └── 10.0.11.0/24
│
└── Private Subnet B
    └── 10.0.12.0/24
```

Public subnets have a route to the Internet Gateway.

Private subnets currently have dedicated route tables without a default Internet route. This keeps the networking foundation intentionally minimal until the private compute and management architecture is implemented.

### Planned

* IAM roles and instance profiles
* EC2 instances
* Systems Manager-based private server management
* Application Load Balancer
* Target groups
* Health checks
* Required private connectivity for management and application image access

The infrastructure will be implemented using reusable and parameterized Terraform configuration.

---

## Server Configuration

Ansible will be responsible for configuration management after infrastructure provisioning.

Planned responsibilities include:

* Creating deployment users
* Configuring secure server access
* Installing Docker
* Configuring Docker
* Applying server configuration
* Deploying the application
* Configuring monitoring
* Performing post-deployment validation

Private EC2 management will be designed around **AWS Systems Manager** rather than exposing SSH access directly to the public internet.

Ansible roles will be designed to be **idempotent**, allowing configuration to be safely re-applied.

---

## Reproducibility

A primary goal of this project is reproducibility.

The intended final workflow is:

```bash
terraform init
terraform plan
terraform apply
```

followed by server configuration and deployment:

```text
Infrastructure
      ↓
Server Management
      ↓
Ansible Configuration
      ↓
Docker Deployment
      ↓
Application
      ↓
Health Check
      ↓
Running Environment
```

The infrastructure should be possible to recreate from the repository rather than relying on manually configured AWS resources.

At the current stage, the Terraform configuration can be initialized, validated, and planned without provisioning AWS resources.

Example:

```bash
terraform -chdir=terraform init
terraform -chdir=terraform validate
terraform -chdir=terraform plan
```

---

## Security Principles

Security will be considered throughout the implementation.

The project will follow principles such as:

* Least-privilege IAM permissions
* Restricted security group rules
* No unnecessary public access
* Private application compute where applicable
* Managed server access instead of publicly exposed SSH
* Non-root Docker containers where applicable
* Secrets kept outside version control
* Environment-specific configuration
* Explicit infrastructure changes through Terraform
* AI analysis separated from infrastructure execution

The current networking design reflects these principles:

* The application EC2 layer is intended to reside in private subnets.
* The ALB will be internet-facing.
* Application traffic to EC2 will be restricted through security-group relationships.
* Private subnets do not currently expose a default internet route.
* SSH is not exposed through the current security groups.

Sensitive files such as credentials, private keys, Terraform state files, and environment files will not be committed to the repository.

---

## Cost-Aware Design

This project is designed as a portfolio project and therefore prioritizes **low-cost AWS infrastructure**.

Infrastructure decisions will consider:

* AWS free-tier eligibility where applicable
* Avoiding unnecessary managed services
* Minimal compute resources
* Explicit cleanup procedures
* Avoiding resources that continue generating costs after testing
* Evaluating recurring networking costs before implementation
* Using private connectivity only where it provides a clear architectural benefit

The project intentionally does **not** provision a NAT Gateway as part of the current networking foundation.

When private EC2 management and application connectivity are implemented, the project will evaluate the cost and architectural trade-offs of options such as:

* Systems Manager connectivity
* VPC interface endpoints
* ECR/S3 connectivity
* NAT Gateway-based egress

Before deploying the complete environment, AWS resource costs and cleanup requirements will be documented.

---

## Development Workflow

The project is being developed incrementally.

Each stage introduces and validates a specific part of the platform:

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
Compute & Load Balancer
        ↓
Stage 6
Ansible Configuration
        ↓
Stage 7
Docker Deployment
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

Each stage is validated before moving to the next stage.

---

## Current Stage

### Stage 3 — AWS Networking ✅

Completed:

* VPC with `10.0.0.0/16` CIDR
* Two public subnets across multiple Availability Zones
* Two private subnets across multiple Availability Zones
* Internet Gateway
* Public route table
* Private route tables
* Route table associations
* Application Load Balancer security group
* Private EC2 security group
* Security-group-based application traffic rules
* Terraform formatting and validation
* Terraform plan validation

Current Terraform plan:

```text
Plan: 15 to add, 0 to change, 0 to destroy.
```

No AWS infrastructure has been provisioned yet.

The current stage intentionally stops at the **networking foundation**. Private server management, IAM, compute, load balancing, and the required private connectivity will be designed in subsequent stages.

---

## Status

🚧 **Project under development**

**Completed:**

* Stage 1 — Project Initialization
* Stage 2 — Terraform Foundation
* Stage 3 — AWS Networking

**Current focus:**

* Stage 4 — Security & IAM

**Upcoming:**

* EC2 and load balancing
* Private server management with AWS Systems Manager
* Ansible configuration
* Docker deployment
* Monitoring and validation
* Reproducible automation
* AI Infrastructure Copilot
* AI explanation and failure analysis
* Portfolio documentation

---

## License

This project is licensed under the [MIT License](LICENSE).

