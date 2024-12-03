# terraform/modules/aws/ses/outputs.tf
output "domain_identity_arn" {
  description = "ARN of the SES domain identity"
  value       = aws_ses_domain_identity.main.arn
}

output "email_bucket_arn" {
  description = "ARN of the S3 bucket storing emails"
  value       = aws_s3_bucket.email_storage.arn
}

output "email_bucket_name" {
  description = "Name of the S3 bucket storing emails"
  value       = aws_s3_bucket.email_storage.id
}