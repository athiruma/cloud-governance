variable "input_variables" {
  description = "Contains the information about the instance data"
  type = map
  default = {}
}

variable "region_name" {
  description = "AWS Region to be perform the resource Creation"
  type = string
}

variable "account_id" {
  default = "452958939641"
  type = string
  description = "AWS Account Id"
}

variable "role_name" {
  default = "TestTerrafomRole"
  type = string
  description = "AWS Role Name"
}