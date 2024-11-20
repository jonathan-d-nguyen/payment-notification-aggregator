# Configure AWS Provider
provider "aws" {
  region = "us-west-2"  # Change to your desired region
}

# Create DynamoDB table
resource "aws_dynamodb_table" "venmo_transactions" {
  name           = "VenmoTransactions"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "transaction_id"

  attribute {
    name = "transaction_id"
    type = "S"
  }

  tags = {
    Environment = "production"
    Project     = "venmo-tracking"
  }
}
