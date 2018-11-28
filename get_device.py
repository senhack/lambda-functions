import json
import os
import boto3

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    device_id = event['pathParameters']['device_id']
    
    dynamodb = boto3.resource('dynamodb')

    device_table = dynamodb.Table(os.environ['DEVICE_DATA_TABLE'])
    device = device_table.get_item(
        Key={
            'DeviceId': device_id
        }
    )

    if 'Item' not in device:
        return {
            "statusCode": 403,
            "body": "This is an unknown device"
        }
    
    device['Item']['SoundThreshold'] = int(device['Item']['SoundThreshold'])

    return {
        "statusCode": 200,
        "headers": {
            "access-control-allow-origin": "*"
        },
        "body": json.dumps(device['Item'])
    }

