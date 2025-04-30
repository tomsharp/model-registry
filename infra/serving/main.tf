resource "aws_ecr_repository" "this" {
  name = "${var.ecr_repo_name}"
}

output "ecr_repo_url" {
    value = aws_ecr_repository.this.repository_url
}