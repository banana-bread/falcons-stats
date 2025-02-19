terraform {
  backend "s3" {
    bucket = "falcons-stats-terraform-state"
    key    = "state"
    region = "us-east-1"
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

resource "aws_security_group_rule" "allow_ssh_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.instances.id
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"] # WARNING: This allows SSH from anywhere!
}

resource "aws_key_pair" "falcons_stats_ssh_key" {
  key_name   = "falcons-stats-server-ssh-key"
  public_key = file("${path.module}/falcons-stats-server-key.pub") # INFO: ensure this exists
}

resource "aws_instance" "falcons_stats_server" {
  ami                    = "ami-053a45fff0a704a47"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instances.id]
  key_name               = "falcons-stats-server-key"
  tags = {
    Name = "FalconsStatsEC2Instance"
  }
}
