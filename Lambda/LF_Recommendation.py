import json
import os
from boto3.dynamodb.conditions import Key, Attr
import boto3

dynamodb = boto3.resource('dynamodb')
recommendation_table = dynamodb.Table('user_search')
table = dynamodb.Table('car_info')

def lambda_handler(event, context):
    # TODO implement
    
    current_user = event["queryStringParameters"]["user"]
    #current_user = "yinsongheng@gmail.com"
    response_from_recommendation = recommendation_table.query(
            KeyConditionExpression=Key('email').eq(current_user)
            )
    
    latest_search = response_from_recommendation['Items'][0]['latest_search']
    
    response_car_table = table.scan(
        FilterExpression=Attr('brand').eq(latest_search)
    )
    
    data = []
    for car in response_car_table["Items"]:
        if car["owner"] != current_user:
            data.append(car)
    
    sorted_data = sorted(data, key=lambda x: float(x['score']), reverse=True)[:3]


    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(sorted_data)
    }
