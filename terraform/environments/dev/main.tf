# terraform/environments/dev/main.tf
module "dynamodb" {
  source = "../../modules/aws/dynamodb"
  
  project_name  = var.project_name
  environment   = "dev"
  tags          = local.common_tags
}

module "lambda" {
  source = "../../modules/aws/lambda"
  
  project_name         = var.project_name
  environment          = "dev"
  lambda_zip_path      = var.lambda_zip_path
  dynamodb_table_name  = module.dynamodb.table_name
  dynamodb_table_arn   = module.dynamodb.table_arn
  email_bucket_arn     = module.ses.email_bucket_arn
  tags                 = local