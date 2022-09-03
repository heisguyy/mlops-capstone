terraform {
  required_version = ">=1.0"
  backend "s3"{
    bucket = "tf-state-mlops-capstone"
    key = "mlops-capstone-stg.tfstate"
    region = "eu-central-1"
    encrypt = true
  }
}

provider "aws" {
    region = var.aws_region
}

data "aws_caller_identity" "current_identity" {}

locals {
    account_id = data.aws_caller_identity.current_identity.account_id
}

# logs bucket
module "capstone_logs" {
  source = "./modules/s3"
  bucket_name = "${var.logs_bucket}-${var.project_id}"

}

module "ecr_image" {
  source = "./modules/ecr"
  ecr_repo_name = "${var.ecr_repo_name}_${var.project_id}"
  account_id = local.account_id
  lambda_function_local_path = var.lambda_function_local_path
  docker_image_local_path = var.docker_image_local_path
}

module "lambda" {
  source = "./modules/lambda"
  image_uri = module.ecr_image.image_uri
  lambda_function_name = "${var.lambda_function_name}_${var.project_id}"
}

module "api" {
  source = "./modules/api-gateway"
  endpoint_name = "${var.endpoint_name}_${var.project_id}"
  lambda_arn = module.lambda.arn
  lambda_function_name = module.lambda.function_name
}
