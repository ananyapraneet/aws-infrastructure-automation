resource "aws_security_group" "ecr_endpoint" {
  name        = "aws-infra-ecr-endpoint-sg"
  description = "Security group for ECR VPC interface endpoints"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "HTTPS from private EC2 instances"
    protocol        = "tcp"
    from_port       = 443
    to_port         = 443
    security_groups = [aws_security_group.ec2.id]
  }

  egress {
    description = "Allow outbound traffic"
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "aws-infra-ecr-endpoint-sg"
    Environment = "portfolio"
    ManagedBy   = "terraform"
    Tier        = "private"
  }
}

resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${var.aws_region}.ecr.api"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true

  subnet_ids = [
    aws_subnet.private_a.id
  ]

  security_group_ids = [
    aws_security_group.ecr_endpoint.id
  ]

  tags = {
    Name        = "aws-infra-ecr-api-endpoint"
    Environment = "portfolio"
    ManagedBy   = "terraform"
    Service     = "ecr.api"
  }
}

resource "aws_vpc_endpoint" "ecr_dkr" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${var.aws_region}.ecr.dkr"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true

  subnet_ids = [
    aws_subnet.private_a.id
  ]

  security_group_ids = [
    aws_security_group.ecr_endpoint.id
  ]

  tags = {
    Name        = "aws-infra-ecr-dkr-endpoint"
    Environment = "portfolio"
    ManagedBy   = "terraform"
    Service     = "ecr.dkr"
  }
}
