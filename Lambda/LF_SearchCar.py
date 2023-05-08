'''
Lambda for handling GET /cars
'''

import json
import os
from boto3.dynamodb.conditions import Key, Attr
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3


region = 'us-east-1'
host = "search-cars-hq323ir5mwvjij34ijp3wzituu.us-east-1.es.amazonaws.com"
INDEX = "cars"

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('car_info')

recommendation_table = dynamodb.Table('user_search')
def search_brands(brands):
    def get_awsauth(region, service):
        cred = boto3.Session().get_credentials()
        return AWS4Auth(
            cred.access_key,
            cred.secret_key,
            region,
            service,
            session_token=cred.token
        )

    query = {
        "size":3,
        "query": {
            "bool": {
                "should": []
            }
        }
    }

    for brand in brands:
        query['query']['bool']['should'].append({
            "match": {
                "brand": brand
            }
        }) 
         
    opensearch = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=get_awsauth(region, "es"),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    try:
        response = opensearch.search(body = query, index = INDEX)
        hits = response['hits']['hits']
        car_id_list = []
        for element in hits:
            objectKey = element['_source']['objectKey']
            car_id_list.append(objectKey)
        return car_id_list
    except Exception as err:
        print(f'failed to search table: {err}')
        ret_status = 400
        ret_msg = f'failed to search table: {err}'
        return None


def lambda_handler(event, context):
    print(event)
    global ret_status, ret_msg
    car_brand = []
    search_brand = event["queryStringParameters"]["q"].title()
    car_brand.append(search_brand)
    current_user = event["queryStringParameters"]["user"]

    response_from_recommendation = recommendation_table.query(
                KeyConditionExpression=Key('email').eq(current_user)
                )
    
    if response_from_recommendation["Count"]==0:
        item = {
            "email":current_user,
            "latest_search": search_brand
        }
        insert_table(item)
    else:
        response_update = recommendation_table.update_item(
            Key={
                'email': current_user
            },
            UpdateExpression='set latest_search = :val',
            ExpressionAttributeValues={
                ':val': search_brand
            },
            ReturnValues="UPDATED_NEW"
        )
        
    car_ids = search_brands(car_brand)
    
    if not car_ids:
        print(f'response is No car found')
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps("No car found")
        }
    else:
        res = []
        print(car_ids)
        for key in car_ids:
            response_from_DB = table.query(
                KeyConditionExpression=Key('car_id').eq(key)
            )
            print(response_from_DB['Items'])
            if response_from_DB['Items']:
                res.append({
                    'brand': response_from_DB['Items'][0]['brand'],
                    'model': response_from_DB['Items'][0]['model'],
                    'year': response_from_DB['Items'][0]['year'],
                    'car_id': response_from_DB['Items'][0]['car_id'],
                    'is_available': response_from_DB['Items'][0]['is_available'],
                    'miles': response_from_DB['Items'][0]['miles'],
                    'owner': response_from_DB['Items'][0]['owner']
                })
            print(f'response is {res}')
            # assist with front end
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(res)
        }


def insert_table(item):
    try:
        response = recommendation_table.put_item(Item=item)
    except Exception as err:
        print(f'failed to insert to table: {err}')
        ret_status = 400
        ret_msg = f'failed to insert to table: {err}'
        return False
    return True