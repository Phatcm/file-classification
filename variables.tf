#provider configure
variable "project_name" {
  type = string
  default = "my-project"
}

variable "region" {
  type = string
}

variable "profile" {
  type = string
}

#iam configure
variable "iam_role_name" {
  type = string
}

variable "policies_list" {
  type = list(string)
}

#lambda uploader
variable "lambda_uploader_function_name" {
  type = string
}

variable "lambda_handler" {
  type = string
}

variable "lambda_runtime" {
  type = string
}

variable "lambda_uploader_output_path" {
  type = string
}

variable "lambda_uploader_source_dir" {
  type = string
}

variable "lambda_uploader_filename" {
  type = string
}

#lambda organize
variable "lambda_organize_function_name" {
  type = string
}

variable "lambda_organize_output_path" {
  type = string
}

variable "lambda_organize_source_dir" {
  type = string
}

variable "lambda_organize_filename" {
  type = string
}


#api gateway configure
variable "api_name" {
  type = string
  default = "api_gateway"
}

#dynamodb configure
variable "table_name" {
  type = string
}

variable "hash_key" {
  type = string
}

variable "hash_key_type" {
  type = string
}

variable "range_key" {
  type = string
}

variable "range_key_type" {
  type = string
}

#s3 configure
variable "s3_organize_bucket" {
  type = string
}