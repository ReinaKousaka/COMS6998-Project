import json
import os
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import uuid


'''
Lambda for handling POST /cars
'''



dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('car_info')

host = "search-cars-hq323ir5mwvjij34ijp3wzituu.us-east-1.es.amazonaws.com"
region = "us-east-1"


def insert_opensearch(item):
    try:
        client_OpenSearch = OpenSearch(
                hosts = [{'host': host, 'port':443}],
                http_auth = get_awsauth(region, "es"),
                use_ssl = True,
                verify_certs = True,
                connection_class = RequestsHttpConnection
            )
            
        response_from_opensearch = client_OpenSearch.index(
        index = 'cars',
        body=item)
    
    except Exception as err:
        print(f'failed to insert to table: {err}')
        ret_status = 400
        ret_msg = f'failed to insert to table: {err}'
        return False
    
    return True
    
    

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
        car["score"] = calculate_car_score(car["brand"], car["miles"], car["year"])
        
        # insert to opensearch
        json_object = {
            "objectKey": car['car_id'],
            "brand": car['brand']
        }
        
        es_payload=json.dumps(json_object).encode("utf-8")
        
        response_from_opensearch = insert_opensearch(es_payload)
        
        
        # insert to dynamoDB
        response = insert_table(car)
        # TODO: add image to S3
    except Exception as err:
        print(f'failed to insert to table: {err}')
        ret_status = 400
        ret_msg = f'failed to insert to table: {err}'

    # Return a success response
    if response and response_from_opensearch:
        return {
            'statusCode': ret_status,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps(ret_msg)
        }
    

def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
                    cred.secret_key,
                    region,
                    service,
                    session_token=cred.token)


def calculate_car_score(brand, mileage, year):
    score = 0
    
    # Brand score
    if brand == 'Bmw' or brand == 'Benz':
        score += 4  # High brand score
    else:
        score += 3  # Low brand score
    
    # Mileage score
    if int(mileage) < 5000:
        score += 2  # High mileage score
    
    # Year score
    if int(year) >= 2020:
        score += 2  # High year score
    
    # Scale the score to a range of 0-5
    scaled_score = round((score / 7) * 5,2)
    
    return str(scaled_score)
