variable "table_name" {
  type = string
  default = "my-table"
}

variable "hash_key" {
  type = string
}

variable "hash_key_type" {
  type = string
  default = "S"
}

variable "range_key" {
  type = string
}

variable "range_key_type" {
  type = string
  default = "S"
}