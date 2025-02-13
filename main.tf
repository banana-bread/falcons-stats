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

resource "aws_instance" "falcons_stats_server" {
  ami                    = "ami-085ad6ae776d8f09c"
  instance_type          = "t2.micro"
  security_groups        = [aws_security_group.instances.name]
  vpc_security_group_ids = [aws_security_group.instances.id]

  tags = {
    Name = "FalconsStatsEC2Instance"
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