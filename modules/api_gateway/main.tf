resource "aws_apigatewayv2_api" "api_gateway" {
  name          = var.api_name
  protocol_type = "HTTP"
  #target        = var.lambda_function_arn
}

resource "aws_apigatewayv2_stage" "api_stage" {
  api_id      = aws_apigatewayv2_api.api_gateway.id
  name        = "$default"
  deployment_id = aws_apigatewayv2_deployment.api_deployment.id
}

resource "aws_apigatewayv2_authorizer" "api_authorizer" {
  api_id                            = aws_apigatewayv2_api.api_gateway.id
  authorizer_type                   = "REQUEST"
  authorizer_uri                    = var.lambda_invoke_arn
  identity_sources                  = ["$request.header.Authorization"]
  name                              = "lambda-authorizer"
  authorizer_payload_format_version = "1.0"
}

resource "aws_apigatewayv2_integration" "api_integration" {
  api_id           = aws_apigatewayv2_api.api_gateway.id
  integration_type = "AWS_PROXY"

  integration_method = "POST"
  integration_uri    = var.lambda_invoke_arn
}

resource "aws_apigatewayv2_route" "api_route" {
  api_id    = aws_apigatewayv2_api.api_gateway.id
  route_key = "POST /files"

  target = "integrations/${aws_apigatewayv2_integration.api_integration.id}"
}

resource "aws_apigatewayv2_deployment" "api_deployment" {
  api_id      = aws_apigatewayv2_api.api_gateway.id
  description = "Example deployment"

  triggers = {
    redeployment = sha1(join(",", tolist([
      jsonencode(aws_apigatewayv2_integration.api_integration),
      jsonencode(aws_apigatewayv2_route.api_route),
    ])))
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Permission
resource "aws_lambda_permission" "apigw" {
	action        = "lambda:InvokeFunction"
	function_name = var.lambda_function_arn
	principal     = "apigateway.amazonaws.com"

	source_arn = "${aws_apigatewayv2_api.api_gateway.execution_arn}/*/*"
}