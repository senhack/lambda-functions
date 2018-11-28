import json
import os
import boto3

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')

    location_table = dynamodb.Table(os.environ['LOCATION_DATA_TABLE'])
    locations = location_table.scan()

    return {
        "statusCode": 200,
        "headers": {
            "access-control-allow-origin": "*"
        },
        "body": json.dumps(locations['Items'])
    }
