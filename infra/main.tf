terraform {
  backend "s3" {
    bucket = "terraform-commons-bucket"
    key    = "model-registry/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      app = var.app_name
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
  bucket = "${var.app_name}-${resource.random_string.this.result}"
}

module "serving" {
  source = "./serving"
  ecr_repo_name = "${var.app_name}-${resource.random_string.this.result}"
}