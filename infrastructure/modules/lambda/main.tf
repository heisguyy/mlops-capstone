resource "aws_lambda_function" "lambda_function" {
  function_name = var.lambda_function_name

  image_uri = var.image_uri
  package_type = "Image"
  role = aws_iam_role.lambda_role.arn

  timeout = 180
}
