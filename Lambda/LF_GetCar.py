import json
import boto3
from boto3.dynamodb.conditions import Attr


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('car_info')


def lambda_handler(event, context):
    print(f'event is {event}')

    # parse input
    response = table.scan(
        FilterExpression=Attr('owner').eq(event['queryStringParameters']['owner'])
    )

    # Print the results
    res = []
    for item in response['Items']:
        print(f'item is {item}')
        res.append(item)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(res)
    }
