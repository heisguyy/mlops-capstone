output "function_name" {
  description = "Name of lambda function"
  value = aws_lambda_function.lambda_function.function_name
}

output "arn" {
  description = "Lambda function's arn"
  value = aws_lambda_function.lambda_function.invoke_arn
}
