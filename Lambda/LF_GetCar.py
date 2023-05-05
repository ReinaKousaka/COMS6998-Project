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


def search_brands(brands):
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
        print(f'failed to insert to table: {err}')
        ret_status = 400
        ret_msg = f'failed to insert to table: {err}'
        return None
    
    
def lambda_handler(event, context):
    
    print(event)
    global ret_status, ret_msg
    car_brand = ["Byd"]
    
    car_id_list_from_opensearch = search_brands(car_brand)
    
    if not car_id_list_from_opensearch:
        return {
            'statusCode': 200,
            'body': json.dumps("No car found")
        }
    else:
        for key in car_id_list_from_opensearch:
            response_from_DB = table.query(
                KeyConditionExpression=Key('car_id').eq(key)
                )        
            
            car_model = response_from_DB['Items'][0]["model"]
            car_year = response_from_DB['Items'][0]["year"]
            car_available = response_from_DB['Items'][0]["is_available"]
        
        
        return {
            'statusCode': 200,
            'body': json.dumps(str(car_model)+str(car_year)+str(car_available))
        }


def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
                    cred.secret_key,
                    region,
                    service,
                    session_token=cred.token)
