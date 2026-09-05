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

The primary goal is to make the infrastructure **reproducible, automated, explainable, and cost-conscious**.

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
              │  │        │           │  │
              │  │       ALB          │  │
              │  └────────┼───────────┘  │
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
    ├── Configure SSH
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
│   └── Infrastructure as Code
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

* VPC
* Public subnets
* Private subnets
* Route tables
* Internet Gateway
* Security groups
* IAM roles and instance profiles
* EC2 instances
* Application Load Balancer
* Target groups
* Health checks

The infrastructure will be implemented using reusable and parameterized Terraform configuration.

---

## Server Configuration

Ansible will be responsible for configuration management after infrastructure provisioning.

Planned responsibilities include:

* Creating deployment users
* Configuring SSH
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

The intended workflow is:

```bash
terraform init
terraform plan
terraform apply
```

followed by:

```bash
ansible-playbook -i inventory site.yml
```

and finally:

```text
Docker deployment
        ↓
Application
        ↓
Health check
        ↓
Running environment
```

The infrastructure should be possible to recreate from the repository rather than relying on manually configured AWS resources.

---

## Security Principles

Security will be considered throughout the implementation.

The project will follow principles such as:

* Least-privilege IAM permissions
* Restricted security group rules
* No unnecessary public access
* Non-root Docker containers where applicable
* Secure SSH configuration
* Secrets kept outside version control
* Environment-specific configuration
* Explicit infrastructure changes through Terraform
* AI analysis separated from infrastructure execution

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

Before deploying the complete environment, AWS resource costs and cleanup requirements will be documented.

---

## Development Workflow

The project will be developed incrementally.

Each stage will introduce and validate a specific part of the platform:

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

---

## Status

🚧 **Project under development**

Current stage:

**Stage 1 — Project Initialization**

Completed:

* Repository initialized
* Project structure created
* Git configured
* MIT license added
* Initial `.gitignore` configured

Upcoming:

* Terraform foundation
* AWS networking
* Security and IAM
* EC2 and load balancing
* Ansible configuration
* Docker deployment
* Monitoring and validation
* Reproducible automation
* AI Infrastructure Copilot

---

## License

This project is licensed under the [MIT License](LICENSE).

