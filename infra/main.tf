provider "aws" {
  region = var.region
  default_tags {
    tags = {
      app = "${var.registry_name}-model-registry"
    }
  }
}

resource "random_string" "this" {
  length  = 5
  special = false
  numeric = false
  upper   = false 
}
resource "aws_s3_bucket" "registry_bucket" {
  bucket = "${var.registry_name}-${resource.random_string.this.result}"
}