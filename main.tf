terraform {
  backend "s3" {}
}
resource "aws_instance" "falcons_stats_server" {
  ami           = "ami-085ad6ae776d8f09c"
  instance_type = "t2.micro"

  tags = {
    Name = "FalconsStatsEC2Instance"
  }
}