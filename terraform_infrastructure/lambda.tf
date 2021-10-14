resource "aws_lambda_function" "alexa_skill_lambda_function" {
  function_name    = "alexa-skill-lambda-function"
  filename         = data.archive_file.lambda_zip_file.output_path
  source_code_hash = data.archive_file.lambda_zip_file.output_base64sha256
  handler          = "lambda_handler.handler"
  role             = aws_iam_role.lambda_assume_role.arn
  runtime          = "python3.8"
}

data "archive_file" "lambda_zip_file" {
  output_path = "${path.module}/lambda_zip/lambda.zip"
  source_dir  = "${path.module}/../lambdas/alexa_skill_lambda"
  excludes    = ["__init__.py", "*.pyc"]
  type        = "zip"
}

resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn  = aws_dynamodb_table.earthquake_dynamodb_table.stream_arn
  function_name     = aws_lambda_function.alexa_skill_lambda_function.arn
  starting_position = "LATEST"
}