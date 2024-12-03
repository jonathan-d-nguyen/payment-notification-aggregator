# terraform/modules/aws/dynamodb/outputs.tf
output "table_name" {
  description = "Name of the DynamoDB transactions table"
  value       = aws_dynamodb_table.transactions.name
}

output "table_arn" {
  description = "ARN of the DynamoDB transactions table"
  value       = aws_dynamodb_table.transactions.arn
}

output "gsi_names" {
  description = "Names of the Global Secondary Indexes"
  value = {
    payment_source = "PaymentSourceIndex"
    status        = "StatusIndex"
  }
}