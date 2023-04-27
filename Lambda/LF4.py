'''Lambda for handling POST /cars
'''
import boto3
import json
import uuid


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('car_info')


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
        car = json.loads(event['body'])
        car['car_id'] = str(uuid.uuid1())       # generate unique id
        car['brand'] = car['brand'].title()     # captitalize first letter
        car['is_available'] = True
        # insert to dynamoDB
        response = insert_table(car)
        # TODO: add image to S3, index OpenSearch
    except Exception as err:
        print(f'failed to insert to table: {err}')
        ret_status = 400
        ret_msg = f'failed to insert to table: {err}'

    # Return a success response
    if response:
        return {
            'statusCode': ret_status,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps(ret_msg)
        }
