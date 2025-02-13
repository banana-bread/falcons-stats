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

# project seems dead, should fork it at some point
module "session_manager" {
  source                   = "bridgecrewio/session-manager/aws"
  version                  = "0.4"
  enable_log_to_s3         = false
  enable_log_to_cloudwatch = false
  # these are requied, even though I set logging to false
  access_log_bucket_name   = "dummy-bucket"
  bucket_name              = "dummy-bucket"
}

resource "aws_instance" "falcons_stats_server" {
  ami                    = "ami-085ad6ae776d8f09c"
  instance_type          = "t2.micro"
  iam_instance_profile   = module.session_manager.instance_profile_name
  vpc_security_group_ids = [aws_security_group.instances.id]

  tags = {
    Name = "FalconsStatsEC2Instance"
  }
}
