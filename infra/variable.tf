variable "region" {
  description = "AWS region to deploy the network to."
  type        = string
}

variable "app_name" {
  type        = string
  description = "Name of your model registry (S3 bucket name)"
}