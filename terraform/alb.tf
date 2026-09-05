resource "aws_lb" "app" {
  name               = "aws-infra-alb"
  internal           = false
  load_balancer_type = "application"

  security_groups = [
    aws_security_group.alb.id
  ]

  subnets = [
    aws_subnet.public_a.id,
    aws_subnet.public_b.id
  ]

  tags = {
    Name        = "aws-infra-alb"
    Environment = "portfolio"
    ManagedBy   = "terraform"
    Tier        = "public"
  }
}

resource "aws_lb_target_group" "app" {
  name     = "aws-infra-app-tg"
  port     = 8000
  protocol = "HTTP"

  target_type = "instance"
  vpc_id      = aws_vpc.main.id

  health_check {
    enabled  = true
    path     = "/health"
    port     = "8000"
    protocol = "HTTP"
    matcher  = "200-399"
  }

  tags = {
    Name        = "aws-infra-app-tg"
    Environment = "portfolio"
    ManagedBy   = "terraform"
    Tier        = "private"
  }
}

resource "aws_lb_target_group_attachment" "app" {
  target_group_arn = aws_lb_target_group.app.arn
  target_id        = aws_instance.app.id
  port             = 8000
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}
