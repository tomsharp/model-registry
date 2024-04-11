output "bucket_name" {
    value = resource.aws_s3_bucket.registry_bucket.id
}