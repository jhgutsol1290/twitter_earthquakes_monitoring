import json

import boto3


def handler(event, context):
    print("Event from dynamodb", event)
    return {"statusCode": 200, "body": json.dumps("Event received")}
