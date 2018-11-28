import json
import os
import boto3

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    location_id = event['pathParameters']['location_id']
    
    dynamodb = boto3.resource('dynamodb')

    device_table = dynamodb.Table(os.environ['DEVICE_DATA_TABLE'])
    devices = device_table.scan(
        FilterExpression=Key('LocationId').eq(location_id)
    )

    if 'Items' not in devices:
        return {
            "statusCode": 403,
            "body": "This location either does not exist or it has no devices"
        }
    
    fixed_devices = []
    for device in devices['Items']:
        device['SoundThreshold'] = int(device['SoundThreshold'])
        fixed_devices.append(device)

    return {
        "statusCode": 200,
        "headers": {
            "access-control-allow-origin": "*"
        },
        "body": json.dumps(fixed_devices)
    }

