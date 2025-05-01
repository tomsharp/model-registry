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

resource "aws_s3_bucket" "registry_bucket" {
  bucket = "${var.app_name}"
}

module "serving" {
  source = "./serving"
  ecr_repo_name = "${var.app_name}"
}