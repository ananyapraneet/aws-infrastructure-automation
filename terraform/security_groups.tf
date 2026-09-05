resource "aws_security_group" "alb" {
  name        = "aws-infra-alb-sg"
  description = "Security group for the application load balancer"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP from the internet"
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from the internet"
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow outbound traffic"
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "aws-infra-alb-sg"
    Environment = "portfolio"
    ManagedBy   = "terraform"
    Tier        = "public"
  }
}

resource "aws_security_group" "ec2" {
  name        = "aws-infra-ec2-sg"
  description = "Security group for private application instances"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Application traffic from the load balancer"
    protocol        = "tcp"
    from_port       = 8000
    to_port         = 8000
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "Allow outbound traffic"
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "aws-infra-ec2-sg"
    Environment = "portfolio"
    ManagedBy   = "terraform"
    Tier        = "private"
  }
}
