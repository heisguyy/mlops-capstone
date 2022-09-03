variable "endpoint_name" {
  type = string
}

variable "lambda_arn" {
  type = string
  description = "The arn of the lambda function to invoke."
}

variable "lambda_function_name" {
  type = string
  description = "The name of the lambda function to invoke."
}
