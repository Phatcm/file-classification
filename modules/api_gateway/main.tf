resource "aws_api_gateway_rest_api" "api_gateway" {
  name        = var.api_name
  description = "This is my API for demonstration purposes"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

#files resouces
resource "aws_api_gateway_resource" "files" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  parent_id   = aws_api_gateway_rest_api.api_gateway.root_resource_id
  path_part   = "files"
}

resource "aws_api_gateway_method" "get_files" {
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  resource_id   = aws_api_gateway_resource.files.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_files_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api_gateway.id
  resource_id             = aws_api_gateway_resource.files.id
  http_method             = aws_api_gateway_method.get_files.http_method
  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

resource "aws_api_gateway_method" "post_files" {
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  resource_id   = aws_api_gateway_resource.files.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_files_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api_gateway.id
  resource_id             = aws_api_gateway_resource.files.id
  http_method             = aws_api_gateway_method.post_files.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

resource "aws_api_gateway_deployment" "prod" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  
  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.api_gateway.body))
  }

  lifecycle {
    create_before_destroy = true
  }
  depends_on = [
    aws_api_gateway_method.get_files
  ]
}

resource "aws_api_gateway_stage" "stage_prod" {
  deployment_id = aws_api_gateway_deployment.prod.id
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  stage_name    = "prod"
}

# Permission
resource "aws_lambda_permission" "apigw" {
	action        = "lambda:InvokeFunction"
	function_name = var.lambda_function_name
	principal     = "apigateway.amazonaws.com"

	source_arn = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/*/*"
}