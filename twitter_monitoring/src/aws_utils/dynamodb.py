"""AWS Utils."""
import os
import boto3

DYNAMODB_TABLE: str = os.getenv("DYNAMODB_EARTHQUAKES_TABLE", "TestingTable")
REGION: str = os.getenv("REGION", "us-west-2")

dynamodb_client = boto3.resource("dynamodb", region_name=REGION)


def upload_to_dynamodb(tweet) -> None:
    """Uploading tweet to DynamoDB.

    :param: tweet: Dict: Tweet streamed by a user
    :return None
    """
    print(f"Inserting tweet into DynamoDB to table {DYNAMODB_TABLE}")
    table = dynamodb_client.Table(DYNAMODB_TABLE)
    response = table.put_item(Item=tweet)
    print(f"Record inserted to DB {response}")
