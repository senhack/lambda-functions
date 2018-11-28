import json
import boto3
import os

def lambda_handler(event, context):
    json_body = event['body']

    dynamodb = boto3.resource('dynamodb')
    
    device_table = dynamodb.Table(os.environ['DEVICE_DATA_TABLE'])
    device = device_table.get_item(
        Key={
            'DeviceId': json_body['DeviceId']
        }
    )

    if 'Item' not in device:
        return {
            "statusCode": 403,
            "body": "This is an unknown device"
        }

    audio_table = dynamodb.Table(os.environ['AUDIO_DATA_TABLE'])
    audio_table.put_item(
        Item=json_body
    )
    
    return {
        "statusCode": 200,
        "headers": {
            "access-control-allow-origin": "*"
        },
        "body": json.dumps(json_body)
    }

