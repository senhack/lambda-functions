import json
import os
import boto3

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    location_id = event['pathParameters']['location_id']
    
    dynamodb = boto3.resource('dynamodb')

    location_table = dynamodb.Table(os.environ['LOCATION_DATA_TABLE'])
    location = location_table.get_item(
        Key={
            'LocationId': location_id
        }
    )

    if 'Item' not in location:
        return {
            "statusCode": 403,
            "body": "This is an unknown location"
        }
    
    return {
        "statusCode": 200,
        "headers": {
            "access-control-allow-origin": "*"
        },
        "body": json.dumps(location['Item'])
    }

