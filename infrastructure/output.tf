output "endpoint_url" {
  value = module.api.url
}

output "logs_bucket" {
  value = module.capstone_logs.bucket_name
}
