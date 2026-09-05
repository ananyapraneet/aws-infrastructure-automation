resource "aws_iam_role" "ec2" {
  name = "aws-infra-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name        = "aws-infra-ec2-role"
    Environment = "portfolio"
    ManagedBy   = "terraform"
  }
}

resource "aws_iam_instance_profile" "ec2" {
  name = "aws-infra-ec2-profile"
  role = aws_iam_role.ec2.name

  tags = {
    Name        = "aws-infra-ec2-profile"
    Environment = "portfolio"
    ManagedBy   = "terraform"
  }
}

resource "aws_iam_role_policy_attachment" "ec2_ssm" {
  role       = aws_iam_role.ec2.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}
