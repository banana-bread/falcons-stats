terraform {
  backend "s3" {
    bucket = "falcons-stats-terraform-state"
    key    = "state"
    region = "us-east-1"
  }
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "falcons-stats-ec2-terraform-state"
  tags = {
    Name        = "Falcons Stats Terraform State Bucket"
    Environment = "Production"
  }
}

resource "aws_s3_bucket_policy" "terraform_state_policy" {
  bucket = aws_s3_bucket.terraform_state.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = "*",
        Action    = ["s3:GetObject"],
        Resource  = "arn:aws:s3:::falcons-stats-ec2-terraform-state/*"
      }
    ]
  })
}

resource "aws_s3_bucket_versioning" "terraform_state_versioning" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_encryption" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_eip" "falcons_stats_server_ip" {
  instance = aws_instance.falcons_stats_server.id

  tags = {
    Name = "FalconsStatsElasticIP"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_security_group" "instances" {
  name = "falcons-stats-server-security-group"

  tags = {
    Name = "Falcons Stats Security Group"
  }
}

resource "aws_security_group_rule" "allow_http_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.instances.id
  from_port         = 8080
  to_port           = 8080
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_iam_role" "ec2_ssm_role" {
  name = "falcons-stats-ssm-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = { Service = "ec2.amazonaws.com" },
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "ssm_access" {
  name       = "ssm-access"
  roles      = [aws_iam_role.ec2_ssm_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ec2_ssm_profile" {
  name = "falcons-stats-ssm-profile"
  role = aws_iam_role.ec2_ssm_role.name
}

resource "aws_iam_policy" "s3_terraform_state_policy" {
  name        = "s3-terraform-state-policy"
  description = "Allows access to the Terraform state bucket"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
        Resource = [
          "arn:aws:s3:::falcons-stats-terraform-state",
          "arn:aws:s3:::falcons-stats-terraform-state/*"
        ]
      }
    ]
  })
}

resource "aws_iam_policy" "ec2_limited_policy" {
  name        = "ec2-limited-policy"
  description = "Allows limited EC2 access for provisioning instances"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ec2:DescribeInstances",
          "ec2:RunInstances",
          "ec2:TerminateInstances",
          "ec2:CreateTags",
          "ec2:DescribeSecurityGroups"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "github_oidc_role" {
  name = "falcons-stats-github-oidc-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringLike = {
            "token.actions.githubusercontent.com:sub" : "repo:banana-bread/falcons-stats:*"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
  role       = aws_iam_role.github_oidc_role.name
  policy_arn = aws_iam_policy.s3_terraform_state_policy.arn
}

resource "aws_iam_role_policy_attachment" "ec2_policy_attachment" {
  role       = aws_iam_role.github_oidc_role.name
  policy_arn = aws_iam_policy.ec2_limited_policy.arn
}

resource "aws_instance" "falcons_stats_server" {
  ami                    = "ami-085ad6ae776d8f09c"
  instance_type          = "t2.micro"
  iam_instance_profile   = aws_iam_instance_profile.ec2_ssm_profile.name
  vpc_security_group_ids = [aws_security_group.instances.id]

  tags = {
    Name = "FalconsStatsEC2Instance"
  }
}
