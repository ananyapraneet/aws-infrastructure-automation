variable "aws_region" {
  description = "AWS region where infrastructure will be provisioned"
  type        = string
  default     = "ap-south-1"

  validation {
    condition     = length(var.aws_region) > 0
    error_message = "AWS region must not be empty."
  }
}

variable "aws_profile" {
  description = "AWS CLI profile used by Terraform"
  type        = string
  default     = "admin-1"

  validation {
    condition     = length(var.aws_profile) > 0
    error_message = "AWS profile must not be empty."
  }
}
