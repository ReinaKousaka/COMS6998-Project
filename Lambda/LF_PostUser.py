import json
import os
import boto3

'''
Lambda for handling POST /user
'''


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def insert_table(item):
    try:
        response = table.put_item(Item=item)
    except Exception as err:
        print(f'failed to insert to table: {err}')
        ret_status = 400
        ret_msg = f'failed to insert to table: {err}'
        return False
    return True


def lambda_handler(event, context):
    # Extract car information from the API Gateway event
    print(f'event is {event}')
    global ret_status, ret_msg
    ret_status, ret_msg = 200, 'Car has been added to the car_info table.'
    
    try:
        user = json.loads(event['body'])
        # insert to dynamoDB
        response = insert_table(user)
        # TODO: add image to S3
    except Exception as err:
        print(f'failed to insert to table: {err}')
        ret_status = 400
        ret_msg = f'failed to insert to table: {err}'

    return {
        'statusCode': ret_status,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps(ret_msg)
    }
