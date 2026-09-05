resource "aws_security_group" "ssm_endpoint" {
  name        = "aws-infra-ssm-endpoint-sg"
  description = "Security group for Systems Manager VPC interface endpoints"
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
    Name        = "aws-infra-ssm-endpoint-sg"
    Environment = "portfolio"
    ManagedBy   = "terraform"
    Tier        = "private"
  }
}

resource "aws_vpc_endpoint" "ssm" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${var.aws_region}.ssm"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true

  subnet_ids = [
    aws_subnet.private_a.id
  ]

  security_group_ids = [
    aws_security_group.ssm_endpoint.id
  ]

  tags = {
    Name        = "aws-infra-ssm-endpoint"
    Environment = "portfolio"
    ManagedBy   = "terraform"
    Service     = "ssm"
  }
}

resource "aws_vpc_endpoint" "ssmmessages" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${var.aws_region}.ssmmessages"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true

  subnet_ids = [
    aws_subnet.private_a.id
  ]

  security_group_ids = [
    aws_security_group.ssm_endpoint.id
  ]

  tags = {
    Name        = "aws-infra-ssmmessages-endpoint"
    Environment = "portfolio"
    ManagedBy   = "terraform"
    Service     = "ssmmessages"
  }
}
