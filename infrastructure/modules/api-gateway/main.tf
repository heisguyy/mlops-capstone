resource "aws_api_gateway_rest_api" "rest_api" {
  name = var.endpoint_name
}

resource "aws_api_gateway_resource" "gateway_resource" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  parent_id   = aws_api_gateway_rest_api.rest_api.root_resource_id
  path_part   = "{proxy+}"
}




resource "aws_api_gateway_method" "gateway_method_root" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  resource_id = aws_api_gateway_rest_api.rest_api.root_resource_id
  http_method = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "gateway_integration_root" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  resource_id = aws_api_gateway_method.gateway_method_root.resource_id
  http_method = aws_api_gateway_method.gateway_method_root.http_method

  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = var.lambda_arn
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    aws_api_gateway_integration.gateway_integration,
    aws_api_gateway_integration.gateway_integration_root
  ]

  rest_api_id = aws_api_gateway_rest_api.rest_api.id

}

resource "aws_lambda_permission" "gateway_lambda_link" {
  statement_id = "AllowAPIGatewayInvoke"
  action = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.rest_api.execution_arn}/*/*"
}
