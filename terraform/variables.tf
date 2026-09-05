variable "aws_region" {
  description = "AWS region where infrastructure will be provisioned"
  type        = string
  default     = "ap-south-1"

  validation {
    condition     = length(var.aws_region) > 0
    error_message = "AWS region must not be empty."
  }
}
