output "aws_region" {
  description = "AWS region configured for this infrastructure"
  value       = var.aws_region
}

output "ec2_iam_role_name" {
  description = "IAM role name assigned to EC2 instances"
  value       = aws_iam_role.ec2.name
}

output "ec2_instance_profile_name" {
  description = "IAM instance profile name assigned to EC2 instances"
  value       = aws_iam_instance_profile.ec2.name
}

output "ec2_instance_id" {
  description = "Application EC2 instance ID"
  value       = aws_instance.app.id
}

output "ec2_private_ip" {
  description = "Private IP address of the application EC2 instance"
  value       = aws_instance.app.private_ip
}

output "alb_dns_name" {
  description = "Public DNS name of the application load balancer"
  value       = aws_lb.app.dns_name
}

output "ansible_ssm_bucket_name" {
  description = "S3 bucket used by Ansible SSM for module transfers"
  value       = aws_s3_bucket.ansible_ssm.id
}
