terraform {
  backend "s3" {
    bucket = var.s3_bucket_name
    key    = var.s3_bucket_key_name
    region = var.aws_region
  }
}
resource "aws_instance" "falcons_stats_server" {
  ami             = "ami-085ad6ae776d8f09c"
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.instances.name]

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