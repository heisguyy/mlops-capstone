variable "aws_region" {
  description = "AWS region to create resources"
  default = "eu-central-1"
}

variable "project_id" {
    description = "project_id"
    default = "mlops-capstone"
}

variable "logs_bucket" {
  description = "S3 buckets for the logs."
}

variable "lambda_function_local_path" {
  description = ""
}

variable "docker_image_local_path" {
  description = ""
}

variable "ecr_repo_name" {
  description = ""
}

variable "lambda_function_name" {
  description = ""
}

variable "endpoint_name" {
  description = ""
}
