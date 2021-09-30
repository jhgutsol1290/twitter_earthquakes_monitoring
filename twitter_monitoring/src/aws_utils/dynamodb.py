"""AWS Utils."""
import boto3

DYNAMODB_TABLE: str = "TestingTable"
REGION: str = "us-east-1"

dynamodb_client = boto3.resource("dynamodb", region_name=REGION)


def upload_to_dynamodb(tweet) -> None:
    """Uploading tweet to DynamoDB.

    :param: tweet: Dict: Tweet streamed by a user
    :return None
    """
    """ table = dynamodb_client.Table(DYNAMODB_TABLE)
    response = table.put_item(Item=tweet)
    print(f"Response {response}") """
    print("Uploading to DynamoDB -> ", tweet)
