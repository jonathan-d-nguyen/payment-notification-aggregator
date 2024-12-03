# terraform/modules/aws/dynamodb/main.tf

# Main transactions table for storing processed payment data
resource "aws_dynamodb_table" "transactions" {
  name           = "${var.project_name}-transactions-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"  # Use on-demand pricing for unpredictable workloads
  hash_key       = "TransactionId"
  range_key      = "Timestamp"

  # Primary key attributes
  attribute {
    name = "TransactionId"
    type = "S"  # String type for UUID
  }

  attribute {
    name = "Timestamp"
    type = "S"  # String type for ISO8601 timestamp
  }

  # Additional attributes for querying
  attribute {
    name = "PaymentSource"
    type = "S"  # String type for "Venmo" or "Zelle"
  }

  attribute {
    name = "Status"
    type = "S"  # String type for payment status
  }

  # Global Secondary Index for querying by payment source
  global_secondary_index {
    name               = "PaymentSourceIndex"
    hash_key           = "PaymentSource"
    range_key         = "Timestamp"
    projection_type    = "ALL"
  }

  # Global Secondary Index for querying by status
  global_secondary_index {
    name               = "StatusIndex"
    hash_key           = "Status"
    range_key         = "Timestamp"
    projection_type    = "ALL"
  }

  # Enable point-in-time recovery for disaster recovery
  point_in_time_recovery {
    enabled = true
  }

  # Enable server-side encryption using AWS managed key
  server_side_encryption {
    enabled = true
  }

  # Configure TTL for old records (90 days)
  ttl {
    enabled        = true
    attribute_name = "ExpirationTime"
  }

  tags = var.tags
}

# Create CloudWatch alarms for monitoring
resource "aws_cloudwatch_metric_alarm" "dynamodb_throttles" {
  alarm_name          = "${var.project_name}-${var.environment}-dynamodb-throttles"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "ThrottledRequests"
  namespace           = "AWS/DynamoDB"
  period              = "300"
  statistic           = "Sum"
  threshold           = "10"
  alarm_description   = "DynamoDB throttled requests"
  alarm_actions       = var.alarm_notification_arns

  dimensions = {
    TableName = aws_dynamodb_table.transactions.name
  }
}