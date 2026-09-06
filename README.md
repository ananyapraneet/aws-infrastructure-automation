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

The primary goal is to make infrastructure **reproducible, automated, explainable, secure, and cost-conscious**.

---

## Architecture

The infrastructure follows a layered architecture that separates public traffic, private application compute, server management, and infrastructure automation.

```text
                              Internet
                                  │
                                  ▼
                    ┌────────────────────────┐
                    │  Application Load      │
                    │       Balancer         │
                    │      Public :80        │
                    └───────────┬────────────┘
                                │
                                │ :8000
                                ▼
                    ┌────────────────────────┐
                    │       Private EC2      │
                    │                        │
                    │   No Public IP         │
                    │   No Public SSH        │
                    │                        │
                    │       Docker           │
                    │          │             │
                    │     Application        │
                    └──────────┬─────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        SSM Endpoint     ECR API / DKR     S3 Gateway
           :443             :443             Endpoint
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                       AWS Private Services


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
      ┌─────┼──────────────┐
      ▼     ▼              ▼
   Security Config.      Failure
   Analysis  Analysis     Analysis
```

The infrastructure is being implemented incrementally.

### Current implementation

The Terraform foundation currently includes:

* VPC
* Multi-AZ public and private subnets
* Internet Gateway
* Public and private route tables
* Security groups
* IAM role and instance profile
* Private EC2 instance
* Internet-facing Application Load Balancer
* ALB target group and health check
* AWS Systems Manager private connectivity
* ECR private connectivity
* S3 Gateway VPC endpoint

The private EC2 instance does **not** receive a public IP and does not require publicly exposed SSH access.

### Design principles

The architecture intentionally separates:

```text
Internet-facing layer
        ↓
Application Load Balancer
        ↓
Private application layer
        ↓
EC2 + Docker
        ↓
Private AWS service connectivity
```

Terraform and Ansible remain responsible for making infrastructure and configuration changes.

The AI layer is intentionally **read-only with respect to infrastructure changes**: it analyzes infrastructure and recommends changes but does not directly modify AWS resources.

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
    ├── IAM
    ├── EC2
    ├── Load Balancer
    └── Private Service Endpoints
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

The intended workflow is:

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
or use a managed access mechanism such as
AWS Systems Manager Session Manager.
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
│   ├── security_groups.tf
│   ├── iam.tf
│   ├── ec2.tf
│   ├── alb.tf
│   ├── ssm.tf
│   ├── s3_endpoint.tf
│   └── ecr_endpoints.tf
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

The directory structure will continue to evolve as Ansible, Docker, monitoring, and AI functionality are implemented.

---

## Infrastructure Components

### Implemented

#### Networking

* VPC
* Two public subnets across multiple Availability Zones
* Two private subnets across multiple Availability Zones
* Internet Gateway
* Public route table
* Dedicated private route tables
* Route table associations
* ALB security group
* Private EC2 security group

#### IAM

* EC2 IAM role
* EC2 instance profile
* AWS Systems Manager managed-instance permissions

#### Compute

* Amazon Linux 2023 EC2 instance
* `t3.micro` instance type
* Private subnet placement
* No public IP
* No SSH key dependency
* Security-group-based application access

#### Load Balancing

* Internet-facing Application Load Balancer
* Public subnet placement across two Availability Zones
* Application target group
* Port `8000` target configuration
* `/health` health check
* ALB-to-EC2 security-group relationship

#### Private Service Connectivity

The private EC2 architecture uses VPC endpoints instead of requiring a NAT Gateway for the current private service access requirements.

Implemented endpoints:

* AWS Systems Manager interface endpoint
* AWS Systems Manager Messages interface endpoint
* Amazon ECR API interface endpoint
* Amazon ECR Docker Registry interface endpoint
* Amazon S3 Gateway endpoint

This allows the architecture to support private management and private container image access while keeping the application instance without a public IP.

### Network Layout

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
│       ├── EC2
│       ├── SSM Endpoint
│       ├── ECR API Endpoint
│       └── ECR DKR Endpoint
│
└── Private Subnet B
    └── 10.0.12.0/24
```

Public subnets have a route to the Internet Gateway.

Private subnets do not currently have a default internet route.

The current EC2 instance resides in **Private Subnet A**.

The S3 Gateway endpoint is associated with both private route tables, while interface endpoints are currently placed in the private subnet hosting the application instance.

---

## Private Server Management

Private EC2 management is designed around **AWS Systems Manager** rather than exposing SSH access directly to the public internet.

The architecture is:

```text
Private EC2
     │
     │ HTTPS :443
     ▼
SSM VPC Endpoints
     │
     ▼
AWS Systems Manager
     │
     ▼
Session Manager
```

The EC2 instance receives the required IAM permissions through its instance profile.

This design removes the need for:

* Public EC2 IP addresses
* Public SSH access
* SSH key distribution for routine server management

Ansible will later integrate with the private management architecture as part of the server configuration workflow.

---

## Private Container Image Connectivity

The project is designed to support private container image pulls from **Amazon ECR**.

The private connectivity layer consists of:

```text
Private EC2
     │
     ├── ECR API Endpoint
     │
     ├── ECR DKR Endpoint
     │
     └── S3 Gateway Endpoint
```

The ECR interface endpoints provide private access to ECR APIs and Docker registry operations, while the S3 Gateway endpoint provides private access to S3-backed image layers and required AWS repositories.

This avoids making the application instance publicly accessible merely to retrieve container images.

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

### Current Terraform validation

The Terraform configuration can currently be initialized, formatted, validated, and planned without provisioning AWS resources.

Example:

```bash
terraform -chdir=terraform init
terraform -chdir=terraform fmt
terraform -chdir=terraform validate
terraform -chdir=terraform plan
```

The latest validated plan is:

```text
Plan: 30 to add, 0 to change, 0 to destroy.
```

**No AWS infrastructure has been provisioned yet.**

This project intentionally follows a **plan-first workflow** during development. Infrastructure will only be applied during the controlled deployment stage.

---

## Security Principles

Security is considered throughout the implementation.

The project follows principles such as:

* Least-privilege IAM permissions
* Restricted security group rules
* No unnecessary public access
* Private application compute
* Managed server access instead of publicly exposed SSH
* Non-root Docker containers where applicable
* Secrets kept outside version control
* Environment-specific configuration
* Explicit infrastructure changes through Terraform
* AI analysis separated from infrastructure execution

The current architecture reflects these principles:

* The EC2 application layer resides in a private subnet.
* The EC2 instance has no public IP.
* SSH is not exposed through the current security groups.
* The ALB is internet-facing.
* Application traffic to EC2 is restricted to traffic originating from the ALB security group.
* Private subnets do not have a default internet route.
* AWS Systems Manager provides the intended private management path.
* ECR and S3 connectivity is provided through VPC endpoints.
* Sensitive files such as credentials, private keys, Terraform state files, and environment files are excluded from version control.

---

## Cost-Aware Design

This project is designed as a portfolio project and therefore prioritizes **low-cost AWS infrastructure**.

Infrastructure decisions consider:

* AWS free-tier eligibility where applicable
* Minimal compute resources
* Avoiding unnecessary managed services
* Explicit cleanup procedures
* Avoiding resources that continue generating costs after testing
* Evaluating recurring networking costs before implementation
* Using private connectivity only where it provides a clear architectural benefit

### NAT Gateway

The project intentionally does **not** provision a NAT Gateway.

Instead, the current private connectivity architecture uses:

```text
Private EC2
    │
    ├── SSM Interface Endpoints
    ├── ECR Interface Endpoints
    └── S3 Gateway Endpoint
```

This provides the required private service connectivity for the current architecture without introducing a permanent NAT Gateway into the portfolio environment.

Interface VPC endpoints do introduce AWS charges, so endpoint placement is intentionally limited to the private subnet currently hosting the EC2 instance where practical.

The infrastructure will continue to be reviewed for cost before the complete environment is deployed.

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
Stage 5.4
Private Service Connectivity
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

The Terraform workflow currently emphasizes:

```text
Implement
   ↓
terraform fmt
   ↓
terraform validate
   ↓
terraform plan
   ↓
Review
   ↓
Commit
   ↓
Push
```

No infrastructure is provisioned merely as part of the development workflow.

---

## Current Stage

### Stage 5.4 — Private Service Connectivity ✅

Completed:

* VPC networking foundation
* Public and private subnets
* Route tables
* Internet Gateway
* Security groups
* EC2 IAM role and instance profile
* Amazon Linux 2023 EC2 instance
* Private EC2 placement
* No public EC2 IP
* Application Load Balancer
* ALB target group
* Application health check
* AWS Systems Manager interface endpoint
* AWS Systems Manager Messages interface endpoint
* Amazon ECR API interface endpoint
* Amazon ECR Docker Registry interface endpoint
* Amazon S3 Gateway endpoint
* Private application traffic through ALB security-group relationships
* Terraform formatting and validation
* Terraform plan validation
* Git-based incremental implementation

Latest Terraform plan:

```text
Plan: 30 to add, 0 to change, 0 to destroy.
```

No AWS infrastructure has been provisioned yet.

### Git Status

The completed infrastructure stages have been committed and pushed to GitHub.

Latest infrastructure commit:

```text
c096750 feat: add private service connectivity
```

---

## Status

🚧 **Project under development**

### Completed

* Stage 1 — Project Initialization
* Stage 2 — Terraform Foundation
* Stage 3 — AWS Networking
* Stage 4 — Security & IAM
* Stage 5.1 — EC2 Compute Foundation
* Stage 5.2 — Application Load Balancer
* Stage 5.3 — Private SSM Management
* Stage 5.4 — Private Service Connectivity

### Current focus

* Preparing the infrastructure foundation for Ansible-based server configuration

### Upcoming

* Ansible configuration
* Docker installation and deployment
* Application deployment
* Monitoring and validation
* Reproducible automation workflow
* Controlled AWS deployment
* AI Infrastructure Copilot
* Terraform plan analysis
* Infrastructure security recommendations
* Infrastructure explanation
* Failure analysis and troubleshooting
* Portfolio documentation and demonstration

---

## License

This project is licensed under the [MIT License](LICENSE).

