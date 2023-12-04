resource "aws_dynamodb_table" "metadata-table" {
    name           = var.table_name
    billing_mode   = "PROVISIONED"
    read_capacity  = 5
    write_capacity = 5
    hash_key       = var.hash_key
    range_key      = var.range_key

    attribute {
        name = var.hash_key
        type = var.hash_key_type
    }

    attribute {
        name = var.range_key
        type = var.range_key_type
    }

    tags = {
    Name        = "files-table"
    Environment = "dev"
    }
}