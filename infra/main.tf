locals {
  config = jsondecode(file("../config.json"))
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
provider "aws" {
  default_tags {
    tags = {
      Owner   = local.config["project_owner"]
      Project = local.config["project_name"]
    }
  }
}

resource "aws_s3_bucket" "model_registry_bucket" {
  bucket = local.config["registry_bucket_name"]
}
