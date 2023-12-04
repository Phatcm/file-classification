terraform {
  required_version = ">=1.0.0"
}

locals {
  name = var.project_name
}

provider "aws" {
  region = var.region
  profile = var.profile
}

module "iam_role" {
  source = "./modules/iam_role"
  iam_role_name = var.iam_role_name
  policies_list = var.policies_list
}

module "lambda_uploader" {
  source = "./modules/lambda"
  lambda_function_name = var.lambda_uploader_function_name
  lambda_handler = var.lambda_handler
  lambda_runtime = var.lambda_runtime
  lambda_role_arn = module.iam_role.iam_role_arn
  output_path = var.lambda_uploader_output_path
  source_dir = var.lambda_uploader_source_dir
  filename = var.lambda_uploader_filename
}

# module "lambda_oganize" {
#   source = "./modules/lambda"
#   lambda_function_name = var.lambda_organize_function_name
#   lambda_handler = var.lambda_handler
#   lambda_runtime = var.lambda_runtime
#   lambda_role_arn = module.iam_role.iam_role_arn
#   output_path = var.lambda_organize_output_path
#   source_dir = var.lambda_organize_source_dir
#   filename = var.lambda_organize_filename
# }

module "api_gateway" {
  source = "./modules/api_gateway"
  api_name = var.api_name
  lambda_function_name = module.lambda_uploader.lambda_function_name
  lambda_function_arn = module.lambda_uploader.lambda_function_arn
  lambda_invoke_arn = module.lambda_uploader.lambda_invoke_arn
}

module "dynamodb" {
  source = "./modules/dynamodb"
  table_name = var.table_name
  hash_key = var.hash_key
  hash_key_type = var.hash_key_type
  range_key = var.range_key
  range_key_type = var.range_key_type
}

module "s3_bucket" {
  source = "./modules/s3"
  s3_organize_bucket = var.s3_organize_bucket
}
