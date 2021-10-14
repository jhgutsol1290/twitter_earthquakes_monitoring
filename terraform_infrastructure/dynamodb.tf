resource "aws_dynamodb_table" "earthquake_dynamodb_table" {
  name             = "TwitterEarthquakes"
  read_capacity    = 5
  write_capacity   = 5
  hash_key         = "user_screen_name"
  range_key        = "created_at"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "user_screen_name"
    type = "S"
  }

  attribute {
    name = "created_at"
    type = "S"
  }
}