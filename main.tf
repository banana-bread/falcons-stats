terraform {
  backend "s3" {
    bucket = "falcons-stats-terraform-state"
    key    = "state"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

# Create IAM role
resource "aws_iam_role" "ssm_role" {
  name = "falcons-ssm-role"
  
  # Trust relationship policy that allows EC2 to assume this role
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "Falcons-SSM-Role"
  }
}

# Attach the AWS managed SSM policy to the role
resource "aws_iam_role_policy_attachment" "ssm_policy" {
  role       = aws_iam_role.ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Create an instance profile with a unique name
resource "aws_iam_instance_profile" "ssm_instance_profile" {
  name = "falcons-ssm-instance-profile"
  role = aws_iam_role.ssm_role.name
}

# Get default VPC information
data "aws_vpc" "default" {
  default = true
}

# Get default subnet in the VPC
data "aws_subnet" "default" {
  vpc_id            = data.aws_vpc.default.id
  default_for_az    = true
  availability_zone = "us-east-1a"
}

# Security group definition
resource "aws_security_group" "instances" {
  name   = "falcons-stats-server-sg"
  vpc_id = data.aws_vpc.default.id
  
  # Define ingress rules inline
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP"
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS"
  }
  
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Custom application port"
  }
  
  # Add an egress rule to allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Falcons Stats Security Group"
  }
}

# Define a network interface
resource "aws_network_interface" "falcons_stats_interface" {
  subnet_id       = data.aws_subnet.default.id
  security_groups = [aws_security_group.instances.id]
  
  tags = {
    Name = "falcons-stats-network-interface"
  }
}

# EC2 instance with explicit IAM role attachment
resource "aws_instance" "falcons_stats_server" {
  ami           = "ami-0bc72bd3b8ba0b59d"
  instance_type = "t4g.micro"
  
  # Attach network interface with public IP
  network_interface {
    network_interface_id = aws_network_interface.falcons_stats_interface.id
    device_index         = 0
  }
  
  # IAM instance profile - explicit reference
  iam_instance_profile = aws_iam_instance_profile.ssm_instance_profile.name
  
  # Configure metadata options
  metadata_options {
    http_endpoint               = "enabled"
    http_put_response_hop_limit = 2
    http_tokens                 = "required"
  }
  
  # Configure credit specification
  credit_specification {
    cpu_credits = "standard"
  }
  
  # Add explicit dependencies
  depends_on = [
    aws_iam_instance_profile.ssm_instance_profile,
    aws_iam_role_policy_attachment.ssm_policy,
    aws_network_interface.falcons_stats_interface
  ]
  
  tags = {
    Name = "FalconsStatsEC2Instance"
  }
}

# Create an Elastic IP for the instance
resource "aws_eip" "falcons_stats_server_ip" {
  domain   = "vpc"
  
  # Associate with the network interface instead of instance directly
  network_interface = aws_network_interface.falcons_stats_interface.id
  
  depends_on = [
    aws_instance.falcons_stats_server
  ]
  
  tags = {
    Name = "FalconsStatsElasticIP"
  }
}

# Output values for verification
output "instance_id" {
  value = aws_instance.falcons_stats_server.id
}

output "instance_arn" {
  value = aws_instance.falcons_stats_server.arn
}

output "instance_profile" {
  value = aws_instance.falcons_stats_server.iam_instance_profile
}

output "public_ip" {
  value = aws_eip.falcons_stats_server_ip.public_ip
}