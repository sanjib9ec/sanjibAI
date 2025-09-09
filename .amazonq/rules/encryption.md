# S3 buckets must be encrypted

Description:
All AWS S3 buckets created in IaC must enable server-side encryption and block public access.

Applies-to:
**/*.tf, **/*.yaml, **/*.yml, **/templates/**

Rule:
If an S3 bucket resource is created without 'server_side_encryption_configuration' or equivalent, flag as HIGH severity.

Examples:
BAD:
resource "aws_s3_bucket" "b" {
  bucket = "my-bucket"
}

GOOD:
resource "aws_s3_bucket" "b" {
  bucket = "my-bucket"
  server_side_encryption_configuration {
    rule { apply_server_side_encryption_by_default { sse_algorithm = "aws:kms" } }
  }
  acl = "private"
}

Severity: HIGH
