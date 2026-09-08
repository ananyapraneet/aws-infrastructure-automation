# AWS Infrastructure Automation Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Reproducible AWS infrastructure provisioning, server configuration, application deployment, infrastructure validation, and infrastructure analysis using **Terraform, Ansible, Docker, Amazon ECR, AWS Systems Manager, Make, and AI-assisted infrastructure analysis**.

## Overview

This project demonstrates a production-oriented approach to automating AWS infrastructure from provisioning through application deployment and validation.

The platform combines:

* **Terraform** for infrastructure provisioning
* **Ansible** for server configuration and configuration management
* **Docker** for application containerization and Ansible controller isolation
* **Amazon ECR** for private container image storage
* **AWS Systems Manager** for private server management
* **Make** for a simplified operator interface
* **AWS** for cloud infrastructure and managed connectivity
* **AI Infrastructure Copilot** for planned infrastructure analysis, security recommendations, configuration explanations, and failure analysis

The infrastructure is intentionally designed without public SSH access and without a NAT Gateway.

Private EC2 instances are managed through **AWS Systems Manager Session Manager**, while private container images are pulled through **VPC endpoints**.

Stage 9 introduces a reproducible operator workflow that combines infrastructure provisioning, configuration, deployment, and validation behind a small set of `make` commands.

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
                        └────────┬────────┘
                                 │
                                 │ HTTP :8000
                                 ▼
                    ┌─────────────────────────┐
                    │      Private EC2        │
                    │     Amazon Linux 2023   │
                    │                         │
                    │       Docker            │
                    │          │              │
                    │          ▼              │
                    │    Flask Application    │
                    │       :8000             │
                    └──────────┬──────────────┘
                               │
                    ┌──────────┴───────────┐
                    │                      │
                    ▼                      ▼
              SSM Endpoints          ECR Endpoints
                    │                      │
                    │                      │
                    ▼                      ▼
             AWS Systems Manager      Amazon ECR
                    ▲
                    │
                    │ AWS SSM
                    │
          ┌─────────┴─────────┐
          │ Dockerized        │
          │ Ansible Controller│
          └─────────┬─────────┘
                    ▲
                    │
             Makefile Interface
                    ▲
                    │
              Developer / Operator
```

The architecture separates:

* **Public traffic** through the Application Load Balancer
* **Private application execution** on EC2
* **Private server management** through AWS Systems Manager
* **Private container image access** through ECR VPC endpoints
* **Infrastructure provisioning** through Terraform
* **Configuration management** through Ansible
* **Application deployment** through Docker and ECR
* **Post-deployment validation** through Ansible
* **Operator workflow** through Make

---

# Core Workflow

Stage 9 provides a simplified operator interface around the complete infrastructure lifecycle.

```text
make provision
       │
       ▼
   Terraform
       │
       ▼
  AWS Infrastructure
       │
       ▼
make configure
       │
       ▼
 Ansible via SSM
       │
       ▼
 Private EC2
       │
       ▼
make deploy
       │
       ├── Docker Build
       │
       ├── ECR Authentication
       │
       ├── ECR Push
       │
       └── Ansible Deployment via SSM
       │
       ▼
 Running Application
       │
       ▼
make validate
       │
       ▼
Infrastructure + Application Validation
```

The individual responsibilities remain separated while the Makefile provides a convenient operator interface.

---

# Reproducible Automation

Stage 9 introduces a Makefile that acts as the primary operator interface.

Available commands:

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
| `make configure` | Configure private EC2 servers with Ansible    |
| `make deploy`    | Build, tag, push, and deploy the application  |
| `make validate`  | Validate infrastructure and application state |
| `make destroy`   | Destroy provisioned AWS infrastructure        |

The workflow intentionally separates:

```text
Provision
   ↓
Configure
   ↓
Deploy
   ↓
Validate
```

This makes individual lifecycle stages independently executable and easier to troubleshoot.

---

# Git-Based Application Deployment

Application images are tagged using the current Git commit SHA.

```text
Git Commit
     │
     ▼
Short Commit SHA
     │
     ▼
Docker Build
     │
     ▼
Amazon ECR
     │
     ▼
Private EC2
```

The Makefile automatically derives the image tag:

```makefile
IMAGE_TAG ?= $(shell git rev-parse --short HEAD)
```

For example:

```text
d0a00b8
```

The resulting image is pushed to ECR as:

```text
aws-infrastructure-app:d0a00b8
```

The ECR repository uses **immutable image tags**, preventing an existing deployment tag from being overwritten.

This provides a simple deployment traceability model:

```text
Git Commit
    ↓
Docker Image
    ↓
ECR Image Tag
    ↓
EC2 Deployment
```

---

# Deployment Flow

The `make deploy` command performs the complete application deployment workflow.

```text
Git commit SHA
      │
      ▼
Docker build
      │
      ▼
ECR authentication
      │
      ▼
Immutable ECR tag
      │
      ▼
Push image
      │
      ▼
Ansible via SSM
      │
      ▼
Private EC2
      │
      ▼
Docker pull
      │
      ▼
Container replacement
      │
      ▼
Running application
```

The deployment process is intentionally separate from Terraform.

Terraform manages infrastructure.

Docker and ECR manage the application image.

Ansible manages application deployment on the server.

---

# Docker Application Deployment

The application is packaged as a lightweight Docker image.

Application:

```text
Flask
  │
  ▼
Docker
  │
  ▼
Port 8000
```

The application exposes:

```text
GET /
GET /health
```

Example health response:

```json
{
  "status": "healthy"
}
```

The application container includes a Docker health check against `/health`.

The container also runs as a non-root user.

---

# AI Infrastructure Copilot

> **Planned — Stage 10**

The project is designed to evolve into an **AI Infrastructure Copilot**.

The AI layer will focus on infrastructure analysis rather than directly modifying production infrastructure.

Planned capabilities include:

* Terraform configuration analysis
* Infrastructure architecture explanations
* Security recommendations
* Cost-awareness analysis
* Configuration explanations
* Infrastructure drift analysis
* Deployment diagnostics
* Failure analysis
* Validation failure explanations
* Suggested remediation steps

The intended architecture is:

```text
                    AI Infrastructure Copilot
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
           Terraform       Ansible       Validation
             Files          Files           Results
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                     Read-Only Analysis
                              │
                              ▼
                  Recommendations / Explanation
```

The AI layer will initially remain **read-only with respect to infrastructure changes**.

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

## Application

* Python
* Flask
* Docker

## Automation

* Make
* Git
* Bash

## Planned AI Layer

* Infrastructure analysis
* Configuration explanation
* Security recommendations
* Failure analysis
* AI-assisted troubleshooting

---

# Project Structure

```text
aws-infrastructure-automation/
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── ansible/
│   ├── ansible.cfg
│   │
│   ├── inventory/
│   │   └── hosts.yml
│   │
│   ├── site.yml
│   │
│   └── roles/
│       ├── user_setup/
│       ├── ssh_hardening/
│       ├── system_config/
│       ├── docker/
│       ├── security_hardening/
│       ├── application/
│       └── validation/
│
├── terraform/
│   ├── providers.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── networking.tf
│   ├── security.tf
│   ├── iam.tf
│   ├── ec2.tf
│   ├── alb.tf
│   ├── endpoints.tf
│   └── ecr.tf
│
├── Makefile
│
├── Dockerfile
│
├── .gitignore
│
└── README.md
```

---

# Infrastructure Components

The AWS environment currently contains:

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

---

# Network Layout

```text
VPC
10.0.0.0/16
│
├── Public Subnet
│   ├── 10.0.1.0/24
│   └── 10.0.2.0/24
│
└── Private Subnets
    ├── 10.0.11.0/24
    │   └── EC2
    │
    └── 10.0.12.0/24
```

The Application Load Balancer is placed in the public subnets.

The application EC2 instance is placed in a private subnet.

There is intentionally **no direct public access to the EC2 instance**.

---

# Private Server Management

The EC2 instance does not expose SSH to the internet.

Instead, Ansible connects through AWS Systems Manager.

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

The EC2 instance uses:

```text
AmazonSSMManagedInstanceCore
```

This provides a secure management path without requiring:

* Public IP addresses
* Internet-facing SSH
* Bastion hosts
* SSH key distribution

---

# Docker-Based Ansible Controller

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

The controller uses pinned versions for its core Ansible dependencies and collections.

This provides:

* Reproducible Ansible execution
* Linux-based process behavior
* Host Python isolation
* Consistent dependencies
* Portable automation
* Reliable Ansible-over-SSM execution

The controller image is:

```text
aws-infra-ansible
```

---

# Ansible Configuration

The main Ansible playbook separates infrastructure configuration, deployment, and validation using tags.

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

This allows the automation to execute only the required lifecycle stage.

For example:

```bash
ansible-playbook -i inventory/hosts.yml site.yml --tags configure
```

or:

```bash
ansible-playbook -i inventory/hosts.yml site.yml --tags deploy
```

or:

```bash
ansible-playbook -i inventory/hosts.yml site.yml --tags validate
```

The Makefile exposes these operations through:

```bash
make configure
make deploy
make validate
```

---

# Application Deployment Role

The Ansible application role is responsible for deploying the selected ECR image.

The deployment sequence is:

```text
Login to ECR
     ↓
Pull application image
     ↓
Stop existing container
     ↓
Start new container
```

The image repository and image tag are supplied dynamically by the Makefile.

Example:

```text
ecr_repository_url=<Terraform ECR output>
image_tag=<Git commit SHA>
aws_region=ap-south-1
```

This avoids hardcoding the deployed image version into the playbook.

---

# Monitoring & Validation

Stage 8 introduced infrastructure and application validation.

The validation role checks:

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
* Running container image matches deployed image
* Application Load Balancer `/health` endpoint

The final Stage 9 validation run completed successfully:

```text
PLAY RECAP

app : ok=22 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

The validation confirmed the deployed application image and end-to-end ALB health.

---

# Private Container Image Connectivity

The EC2 instance does not require public internet access to pull the application image.

Private connectivity is provided through VPC endpoints.

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

The environment includes:

* ECR API interface endpoint
* ECR Docker Registry interface endpoint
* S3 gateway endpoint

This allows the private EC2 instance to retrieve container images without requiring a NAT Gateway.

---

# Reproducibility

The project is designed around repeatable infrastructure and deployment operations.

## Infrastructure

```bash
make provision
```

runs:

```text
terraform init
      ↓
terraform apply
```

## Infrastructure Planning

```bash
make plan
```

runs:

```text
terraform init
      ↓
terraform plan
```

## Server Configuration

```bash
make configure
```

runs the Dockerized Ansible controller with:

```text
--tags configure
```

## Application Deployment

```bash
make deploy
```

performs:

```text
Docker Build
    ↓
ECR Login
    ↓
Git SHA Tag
    ↓
ECR Push
    ↓
Ansible Deploy
    ↓
AWS SSM
    ↓
Private EC2
```

## Validation

```bash
make validate
```

runs the validation role with:

```text
--tags validate
```

and dynamically supplies:

* ECR repository URL
* AWS region
* deployed image tag
* Application Load Balancer DNS name

## Destruction

```bash
make destroy
```

runs:

```text
terraform destroy
```

---

# Host Prerequisites

The Makefile expects the following tools to be available on the operator machine:

* Docker
* AWS CLI
* Terraform
* Make
* Git

AWS credentials must also be configured.

The current Makefile defaults to:

```text
AWS_PROFILE=admin-1
AWS_REGION=ap-south-1
```

The Ansible controller image must be available locally:

```text
aws-infra-ansible
```

The Ansible controller itself is Dockerized, but Docker and AWS CLI are still used by the host for operations such as:

* Building the application image
* Authenticating to ECR
* Pushing the image
* Running the Ansible controller

---

# Security Principles

The project follows several security-oriented design principles.

### No Public EC2 Access

The EC2 instance does not expose SSH to the internet.

### Private Server Management

AWS Systems Manager is used instead of public SSH.

### Private Application Server

The application runs on a private EC2 instance.

### Security Group Separation

The EC2 security group permits application traffic only from the Application Load Balancer security group.

### Non-Root Containers

The application container runs as a non-root user.

### Immutable ECR Tags

ECR image tags are immutable.

### ECR Image Scanning

ECR scan-on-push is enabled.

### Least-Privilege IAM

The EC2 instance receives only the permissions required for:

* Systems Manager management
* ECR image retrieval

### Read-Only AI Design

The planned AI layer will analyze infrastructure without directly modifying AWS resources.

---

# Cost-Aware Design

The architecture intentionally avoids unnecessary managed infrastructure costs.

Current design choices include:

* `t3.micro` EC2
* No NAT Gateway
* VPC endpoints for private AWS service connectivity
* Single application instance
* Lightweight Docker images
* Amazon ECR
* Application Load Balancer

The absence of a NAT Gateway is particularly intentional because NAT Gateway hourly and data-processing charges can significantly increase the cost of a small portfolio environment.

Private connectivity is instead provided through VPC endpoints required for the application's AWS dependencies.

---

# Development Workflow

The project is being developed incrementally.

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

# Current Stage

## Stage 9 — Reproducible Automation ✅

Completed:

* Makefile-based operator interface
* `make provision`
* `make plan`
* `make configure`
* `make deploy`
* `make validate`
* `make destroy`
* Dynamic Terraform output retrieval for deployment values
* Git commit SHA image tagging
* Immutable ECR image tags
* Automated Docker image build
* Automated ECR authentication
* Automated ECR image push
* Ansible configure/deploy/validate separation
* Dockerized Ansible controller
* End-to-end application deployment
* End-to-end infrastructure validation
* ALB health validation
* Private EC2 deployment through AWS SSM

The final validation workflow completed successfully with:

```text
app : ok=22 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

---

# Infrastructure Status

| Area                           | Status     |
| ------------------------------ | ---------- |
| Terraform Infrastructure       | ✅ Complete |
| VPC Networking                 | ✅ Complete |
| Security Groups                | ✅ Complete |
| IAM                            | ✅ Complete |
| Private EC2                    | ✅ Complete |
| Application Load Balancer      | ✅ Complete |
| AWS Systems Manager            | ✅ Complete |
| Private ECR Connectivity       | ✅ Complete |
| Ansible Configuration          | ✅ Complete |
| Docker Application Deployment  | ✅ Complete |
| Infrastructure Validation      | ✅ Complete |
| Reproducible Makefile Workflow | ✅ Complete |
| AI Infrastructure Copilot      | 🚧 Planned |
| AI Failure Analysis            | 🚧 Planned |
| Portfolio Documentation        | 🚧 Planned |

---

# Upcoming

## Stage 10 — AI Infrastructure Copilot

Planned capabilities:

* Terraform analysis
* Architecture explanation
* Security recommendations
* Cost analysis
* Configuration explanations
* Infrastructure recommendations

## Stage 11 — AI Explain & Failure Analysis

Planned capabilities:

* Validation failure explanation
* Deployment failure analysis
* Ansible failure analysis
* Infrastructure troubleshooting
* Root-cause analysis
* Suggested remediation

## Stage 12 — Portfolio & Documentation

Planned work:

* Final architecture documentation
* Architecture diagrams
* Deployment documentation
* Troubleshooting guide
* Infrastructure decisions
* Security documentation
* Cost analysis
* GitHub portfolio presentation

---

# Status

### Completed

* Stage 1 — Project Initialization ✅
* Stage 2 — Terraform Foundation ✅
* Stage 3 — AWS Networking ✅
* Stage 4 — Security & IAM ✅
* Stage 5.1 — EC2 Compute Foundation ✅
* Stage 5.2 — Application Load Balancer ✅
* Stage 5.3 — Private SSM Management ✅
* Stage 5.4 — Private Service Connectivity ✅
* Stage 6 — Ansible Configuration ✅
* Stage 7 — Docker Application Deployment ✅
* Stage 8 — Monitoring & Validation ✅
* Stage 9 — Reproducible Automation ✅

### Planned

* Stage 10 — AI Infrastructure Copilot 🚧
* Stage 11 — AI Explain & Failure Analysis 🚧
* Stage 12 — Portfolio & Documentation 🚧

---

# License

This project is licensed under the MIT License.

See [LICENSE](LICENSE) for details.

