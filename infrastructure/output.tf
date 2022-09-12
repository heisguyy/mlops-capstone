output "endpoint_url" {
  value = module.api.url
}

output "logs_bucket" {
  value = module.capstone_logs.bucket_name
}

output "ecr_repo" {
  value = "${var.ecr_repo_name}_${var.project_id}"
}

output "lambda_function" {
  value     = "${var.lambda_function_name}_${var.project_id}"
}
