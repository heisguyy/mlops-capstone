variable "ecr_repo_name" {
  type = string
  description = "ECR repository for docker images"
}

variable "ecr_image_tag" {
  type = string
  description = "Image tag for the container to be deployed"
  default = "latest"
}

variable "lambda_function_local_path" {
  type = string
  description = "Local path to lambda function / python file"
}

variable "docker_image_local_path" {
  type = string
  description = "Local path to dockerfile"
}

variable "region" {
  type = string
  description = "region"
  default = "eu-central-1"
}

variable "account_id" {

}
