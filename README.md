# AWS Infrastructure Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Reproducible AWS infrastructure provisioning and server configuration using **Terraform, Ansible, Docker, and AI-assisted infrastructure analysis**.

## Overview

**AWS Infrastructure Automation** is a DevOps/SRE-focused infrastructure automation platform designed to provision, configure, deploy, and validate a complete application environment on AWS.

The project combines:

* **Terraform** for infrastructure provisioning
* **Ansible** for server configuration and configuration management
* **Docker** for application deployment and Ansible controller isolation
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
        SSM Endpoints     ECR API / DKR     S3 Gateway
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

The infrastructure is implemented incrementally using Terraform and Ansible, with Docker providing an isolated and reproducible automation environment.

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
* S3 bucket used by Ansible's AWS Systems Manager connection

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
    ├── Configure secure server access
    ├── Configure system
    ├── Install Docker
    ├── Configure Docker
    ├── Apply security hardening
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
│   ├── .terraform.lock.hcl
│   ├── providers.tf
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
│   ├── ansible_ssm.tf
│   ├── s3_endpoint.tf
│   └── ecr_endpoints.tf
│
├── ansible/
│   ├── ansible.cfg
│   ├── inventory/
│   │   └── hosts.yml
│   ├── site.yml
│   ├── Dockerfile
│   └── roles/
│       ├── user_setup/
│       ├── ssh_hardening/
│       ├── system_config/
│       ├── docker/
│       └── security_hardening/
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

Ansible uses a role-based architecture so that individual configuration responsibilities remain isolated, reusable, and idempotent.

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

An S3 bucket is also provisioned for Ansible's AWS Systems Manager connection mechanism.

This allows the architecture to support private management and private container image access while keeping the application instance without a public IP.

---

## Network Layout

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

Private EC2 management is designed around **AWS Systems Manager Session Manager** rather than exposing SSH access directly to the public internet.

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

Ansible integrates with this architecture using the `amazon.aws.aws_ssm` connection plugin.

### Ansible over AWS SSM

Ansible does not connect directly to the EC2 instance over SSH.

Instead:

```text
Ansible Controller
       │
       ▼
AWS SSM Connection Plugin
       │
       ▼
AWS Systems Manager
       │
       ▼
Private EC2
```

An S3 bucket is used by the Ansible SSM connection mechanism for transferring required execution data.

This allows Ansible to configure the private EC2 instance without exposing an SSH port to the internet.

---

## Docker-Based Ansible Controller

Ansible is executed from a **Docker-based controller** rather than directly from the macOS host.

The controller image contains:

* Python
* Ansible Core
* `amazon.aws`
* `community.general`
* `ansible.posix`
* Boto3 / Botocore
* AWS Systems Manager Session Manager Plugin

Example:

```bash
docker build -t aws-infra-ansible ansible
```

Ansible playbooks are then executed through the container:

```bash
docker run --rm -it \
  -v "$PWD/ansible:/workspace/ansible" \
  -v "$HOME/.aws:/root/.aws" \
  -e AWS_PROFILE=admin-1 \
  -e AWS_DEFAULT_REGION=ap-south-1 \
  aws-infra-ansible \
  ansible-playbook \
  -i /workspace/ansible/inventory/hosts.yml \
  /workspace/ansible/site.yml
```

### Why Docker is used

During development, the native macOS Ansible controller experienced worker-process crashes when using the AWS SSM connection plugin.

The underlying AWS components themselves were verified independently:

* AWS credentials and Boto3 access worked
* AWS Systems Manager API access worked
* S3 access worked
* Session Manager Plugin worked
* SSM sessions could be established successfully

The instability occurred specifically within the native macOS Ansible worker execution path.

Rather than weakening the infrastructure architecture or exposing SSH access as a workaround, the project uses a **Linux-based Docker Ansible controller**.

This provides:

* A reproducible Ansible execution environment
* Linux-based process behavior for Ansible workers
* Pinned Ansible and collection versions
* Consistent dependencies
* Isolation from the host Python environment
* Reliable Ansible-over-SSM execution

The Docker controller successfully executes the complete role-based playbook against the private EC2 instance.

---

## Ansible Configuration

Ansible configuration is organized using independent roles:

```text
roles/
├── user_setup/
├── ssh_hardening/
├── system_config/
├── docker/
└── security_hardening/
```

The main playbook orchestrates these roles:

```yaml
- name: Configure application servers
  hosts: app_servers
  become: true

  roles:
    - user_setup
    - ssh_hardening
    - system_config
    - docker
    - security_hardening
```

### User Configuration

The `user_setup` role:

* Creates the `deploy` user
* Creates a home directory
* Adds the user to the `wheel` group

### SSH Hardening

The `ssh_hardening` role:

* Disables SSH root login
* Disables SSH password authentication
* Disables empty passwords
* Validates the SSH configuration before applying changes

SSH remains intentionally unavailable from the public internet.

### System Configuration

The `system_config` role:

* Updates installed packages
* Installs essential system utilities
* Configures the system timezone
* Creates `/opt/app`
* Assigns application ownership to the deployment user

### Docker Configuration

The `docker` role:

* Installs Docker
* Adds the deployment user to the Docker group
* Enables Docker at boot
* Starts the Docker service

Docker was successfully verified on the EC2 instance.

### Security Hardening

The `security_hardening` role applies kernel/network security settings using `ansible.posix.sysctl`.

Implemented controls include:

* Disable IPv4 forwarding
* Disable IPv6 forwarding
* Disable ICMP redirects
* Disable secure ICMP redirects
* Disable source routing
* Enable reverse path filtering
* Disable IPv4 ICMP redirects being sent

The resulting configuration was verified directly on the EC2 instance:

```text
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.all.send_redirects = 0
```

The complete Ansible playbook currently executes successfully with:

```text
ok=19
changed=7
unreachable=0
failed=0
skipped=0
rescued=0
ignored=0
```

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

## Reproducibility

A primary goal of this project is reproducibility.

The infrastructure can be initialized, formatted, validated, planned, and provisioned using Terraform:

```bash
terraform -chdir=terraform init
terraform -chdir=terraform fmt
terraform -chdir=terraform validate
terraform -chdir=terraform plan
terraform -chdir=terraform apply
```

Server configuration is then performed through the Docker-based Ansible controller:

```text
Terraform
    ↓
AWS Infrastructure
    ↓
AWS Systems Manager
    ↓
Docker-based Ansible Controller
    ↓
Ansible Roles
    ↓
Server Configuration
    ↓
Docker
    ↓
Application
```

The infrastructure is designed to be recreated from the repository rather than relying on manually configured AWS resources.

### Current Terraform deployment

Terraform has been successfully applied to AWS.

The infrastructure deployment completed successfully with:

```text
30 added
0 changed
0 destroyed
```

The resulting environment includes the VPC, networking, security groups, IAM resources, private EC2 instance, Application Load Balancer, and private AWS service connectivity.

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
* Server hardening through Ansible
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
* SSH root login and password authentication are disabled.
* Network forwarding and source-routing behavior are hardened through Ansible.
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

This provides the required private service connectivity for the current architecture without introducing a permanent NAT Gateway.

Interface VPC endpoints do introduce AWS charges, so endpoint placement is intentionally limited to the private subnet currently hosting the EC2 instance where practical.

The infrastructure will continue to be reviewed for cost before additional services are introduced.

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

The Terraform workflow emphasizes:

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
terraform apply
   ↓
Validate AWS resources
   ↓
Commit
   ↓
Push
```

The Ansible workflow emphasizes:

```text
Implement Role
      ↓
Build Controller
      ↓
Execute via AWS SSM
      ↓
Validate Configuration
      ↓
Review
      ↓
Commit
      ↓
Push
```

---

## Current Stage

### Stage 6 — Ansible Configuration ✅

Completed:

* Docker-based Ansible controller
* Pinned Ansible Core and Ansible collection versions
* AWS SSM Ansible connection
* S3 transfer bucket for Ansible SSM
* Role-based Ansible architecture
* Deployment user creation
* SSH hardening
* System package configuration
* System timezone configuration
* Application directory creation
* Docker installation
* Docker service configuration
* Docker group configuration
* Kernel/network security hardening
* Successful end-to-end Ansible execution over AWS Systems Manager
* Verification of all security hardening parameters

Latest successful Ansible execution:

```text
PLAY RECAP

app : ok=19
      changed=7
      unreachable=0
      failed=0
      skipped=0
      rescued=0
      ignored=0
```

Security hardening was subsequently verified directly on the EC2 instance.

### Infrastructure Status

The AWS infrastructure is currently provisioned and operational for the implemented stages.

The environment includes:

```text
VPC
 ├── Public Subnets
 │    └── Application Load Balancer
 │
 └── Private Subnets
      ├── EC2
      ├── SSM Endpoints
      ├── ECR Endpoints
      └── S3 Gateway Endpoint
```

The EC2 instance is managed privately through AWS Systems Manager.

### Upcoming

* Docker-based application deployment
* Application container deployment
* Monitoring and validation
* Reproducible end-to-end automation workflow
* Controlled deployment workflow
* AI Infrastructure Copilot
* Terraform plan analysis
* Infrastructure security recommendations
* Infrastructure explanation
* Failure analysis and troubleshooting
* Portfolio documentation and demonstration

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
* Stage 6 — Ansible Configuration

### Current focus

* Preparing Docker-based application deployment on the private EC2 instance

### Upcoming

* Stage 7 — Docker Deployment
* Stage 8 — Monitoring & Validation
* Stage 9 — Reproducible Automation
* Stage 10 — AI Infrastructure Copilot
* Stage 11 — AI Explain & Failure Analysis
* Stage 12 — Portfolio & Documentation

---

## License

This project is licensed under the [MIT License](LICENSE).

