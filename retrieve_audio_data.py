import json
import os
import boto3

from boto3.dynamodb.conditions import Key, Attr

def retrieve_data(event, context):
    start_date = event['queryStringParameters']['start_date']
    end_date = event['queryStringParameters']['end_date']
    device_id = event['queryStringParameters']['device_id']
    
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

    table = dynamodb.Table(os.environ['AUDIO_DATA_TABLE'])
    
    results = table.query(
        Select="ALL_ATTRIBUTES",
        KeyConditionExpression=Key('DeviceId').eq(device_id) & Key('RecordingDate').between(start_date, end_date)
    )
    
    return {
        "statusCode": 200,
        "headers": {
            "access-control-allow-origin": "*"
        },
        "body": json.dumps(results['Items'])
    }

