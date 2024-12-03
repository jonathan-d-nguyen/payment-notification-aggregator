# terraform/modules/aws/ses/main.tf
resource "aws_ses_domain_identity" "main" {
  domain = var.domain_name
}

resource "aws_ses_receipt_rule_set" "main" {
  rule_set_name = "${var.project_name}-email-rules"
  depends_on    = [aws_ses_domain_identity.main]
}

resource "aws_ses_receipt_rule" "payment_notifications" {
  name          = "process-payment-notifications"
  rule_set_name = aws_ses_receipt_rule_set.main.rule_set_name
  enabled       = true
  scan_enabled  = true

  recipients = [
    "payments@${var.domain_name}"
  ]

  s3_action {
    bucket_name = aws_s3_bucket.email_storage.id
    position    = 1
  }

  lambda_action {
    function_arn    = var.lambda_function_arn
    position        = 2
    invocation_type = "Event"
  }
}

# S3 bucket for storing raw emails
resource "aws_s3_bucket" "email_storage" {
  bucket = "${var.project_name}-email-storage-${var.environment}"
  
  lifecycle_rule {
    enabled = true
    
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    
    expiration {
      days = 90
    }
  }

  tags = var.tags
}

# S3 bucket policy to allow SES to write emails
resource "aws_s3_bucket_policy" "email_storage" {
  bucket = aws_s3_bucket.email_storage.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowSESPuts"
        Effect = "Allow"
        Principal = {
          Service = "ses.amazonaws.com"
        }
        Action = "s3:PutObject"
        Resource = "${aws_s3_bucket.email_storage.arn}/*"
        Condition = {
          StringEquals = {
            "aws:Referer" = data.aws_caller_identity.current.account_id
          }
        }
      }
    ]
  })
}