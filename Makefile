.PHONY: help provision configure deploy validate destroy plan

SHELL := /bin/bash

AWS_PROFILE ?= admin-1
AWS_REGION ?= ap-south-1
ANSIBLE_IMAGE ?= aws-infra-ansible

TERRAFORM_DIR := terraform
APP_DIR := app

IMAGE_TAG ?= $(shell git rev-parse --short HEAD)

TF_OUTPUT = cd $(TERRAFORM_DIR) && terraform output -raw $(1)

ECR_REPOSITORY := $(shell $(call TF_OUTPUT,ecr_repository_url))
ALB_DNS_NAME := $(shell $(call TF_OUTPUT,alb_dns_name))

ANSIBLE_RUN = docker run --rm -it \
-v "$$(pwd):/workspace" \
-v "$$HOME/.aws:/root/.aws" \
-e AWS_PROFILE=$(AWS_PROFILE) \
-e AWS_DEFAULT_REGION=$(AWS_REGION) \
$(ANSIBLE_IMAGE) \
ansible-playbook \
-i /workspace/ansible/inventory/hosts.yml \
/workspace/ansible/site.yml

help:
	@echo "AWS Infrastructure Automation"
	@echo ""
	@echo "Available commands:"
	@echo "  make provision  - Provision AWS infrastructure with Terraform"
	@echo "  make configure  - Configure servers with Ansible"
	@echo "  make deploy     - Build and deploy the application"
	@echo "  make validate   - Validate infrastructure and deployment"
	@echo "  make plan       - Show Terraform infrastructure changes"
	@echo "  make destroy    - Destroy provisioned AWS infrastructure"

provision:
	cd $(TERRAFORM_DIR) && terraform init
	cd $(TERRAFORM_DIR) && terraform apply

plan:
	cd $(TERRAFORM_DIR) && terraform init
	cd $(TERRAFORM_DIR) && terraform plan

configure:
	$(ANSIBLE_RUN) --tags configure

deploy:
	docker build -t aws-infra-app:$(IMAGE_TAG) $(APP_DIR)
	aws ecr get-login-password \
	--region $(AWS_REGION) \
	--profile $(AWS_PROFILE) | \
	docker login \
	--username AWS \
	--password-stdin $(ECR_REPOSITORY)
	docker tag aws-infra-app:$(IMAGE_TAG) $(ECR_REPOSITORY):$(IMAGE_TAG)
	docker push $(ECR_REPOSITORY):$(IMAGE_TAG)
	$(ANSIBLE_RUN) \
	--tags deploy \
	-e "ecr_repository_url=$(ECR_REPOSITORY)" \
	-e "aws_region=$(AWS_REGION)" \
	-e "image_tag=$(IMAGE_TAG)"

validate:
	$(ANSIBLE_RUN) \
	--tags validate \
	-e "ecr_repository_url=$(ECR_REPOSITORY)" \
	-e "aws_region=$(AWS_REGION)" \
	-e "image_tag=$(IMAGE_TAG)" \
	-e "alb_dns_name=$(ALB_DNS_NAME)"

destroy:
	cd $(TERRAFORM_DIR) && terraform destroy
