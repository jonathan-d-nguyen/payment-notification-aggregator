# Configure AWS SES domain and email receiving
resource "aws_ses_domain_identity" "main" {
  domain = "yourdomain.com"  # Replace with your domain
}

# Configure DNS records for SES domain verification
resource "aws_route53_record" "ses_verification" {
  zone_id = "YOUR_ROUTE53_ZONE_ID"  # Replace with your Route53 zone ID
  name    = "_amazonses.${aws_ses_domain_identity.main.domain}"
  type    = "TXT"
  ttl     = "600"
  records = [aws_ses_domain_identity.main.verification_token]
}

# Create S3 bucket for receiving emails
resource "aws_s3_bucket" "ses_incoming" {
  bucket = "XXXXXXXXXincoming-bucket"
}

# Configure S3 bucket policy to allow SES to write emails
resource "aws_s3_bucket_policy" "ses_incoming" {
  bucket = aws_s3_bucket.ses_incoming.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowSESPuts"
        Effect = "Allow"
        Principal = {
          Service = "ses.amazonaws.com"
        }
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.ses_incoming.arn}/*"
        Condition = {
          StringEquals = {
            "aws:Referer" = data.aws_caller_identity.current.account_id
          }
        }
      }
    ]
  })
}

# Create SES receipt rule set
resource "aws_ses_receipt_rule_set" "main" {
  rule_set_name = "primary-rules"
}

# Create SES receipt rule
resource "aws_ses_receipt_rule" "store" {
  name          = "store"
  rule_set_name = aws_ses_receipt_rule_set.main.rule_set_name
  recipients    = ["user@yourdomain.com"]  # Optional: Specify recipients
  enabled       = true
  scan_enabled  = true
  
  s3_action {
    bucket_name = aws_s3_bucket.ses_incoming.id
    position    = 1
  }

  # Optional: Add SNS notification
  sns_action {
    topic_arn = aws_sns_topic.ses_notifications.arn
    position  = 2
  }
}

# Optional: Create SNS topic for email notifications
resource "aws_sns_topic" "ses_notifications" {
  name = "ses-notifications"
}

# Get current AWS account ID
data "aws_caller_identity" "current" {}

# Activate the rule set
resource "aws_ses_active_receipt_rule_set" "main" {
  rule_set_name = aws_ses_receipt_rule_set.main.rule_set_name
}

# Configure DKIM
resource "aws_ses_domain_dkim" "main" {
  domain = aws_ses_domain_identity.main.domain
}

# Create DKIM DNS records
resource "aws_route53_record" "dkim" {
  count   = 3
  zone_id = "YOUR_ROUTE53_ZONE_ID"  # Replace with your Route53 zone ID
  name    = "${element(aws_ses_domain_dkim.main.dkim_tokens, count.index)}._domainkey.${aws_ses_domain_identity.main.domain}"
  type    = "CNAME"
  ttl     = "600"
  records = ["${element(aws_ses_domain_dkim.main.dkim_tokens, count.index)}.dkim.amazonses.com"]
}

# Configure MX record
resource "aws_route53_record" "mx" {
  zone_id = "YOUR_ROUTE53_ZONE_ID"  # Replace with your Route53 zone ID
  name    = aws_ses_domain_identity.main.domain
  type    = "MX"
  ttl     = "600"
  records = ["10 inbound-smtp.${data.aws_region.current.name}.amazonaws.com"]
}

# Get current AWS region
data "aws_region" "current" {}
