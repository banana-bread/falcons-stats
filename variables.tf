variable "aws_region" {
  description = "The AWS region to deploy resources"
  default     = "us-east-1"
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket to store the Terraform state"
  default     = "falcons-stats-terraform-state"
}

variable "s3_bucket_key_name" {
  description = "The key (path) in the S3 bucket for the Terraform state file"
  default     = "terraform/state"
}