resource "aws_ecr_repository" "app" {
  name                 = "aws-infrastructure-app"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Name        = "aws-infrastructure-app"
    Environment = "portfolio"
    ManagedBy   = "terraform"
  }
}
