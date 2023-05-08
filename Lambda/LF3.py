import json
import os
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from boto3.dynamodb.conditions import Key, Attr
from requests_aws4auth import AWS4Auth
from botocore.vendored import requests
from botocore.exceptions import ClientError

region = 'us-east-1'
host = 'search-cars-hq323ir5mwvjij34ijp3wzituu.us-east-1.es.amazonaws.com'
INDEX = 'cars'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('car_info')

def lambda_handler(event, context):
    print("tHIS IS EVENT", event)
    
    # Grab data from SQS
    sqs = boto3.client('sqs')
    s_queue_s = sqs.get_queue_url(QueueName='CarQueue')
    queue_url = s_queue_s['QueueUrl']
    response_from_sqs = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    #print("SQS RESPONSE", response_from_sqs)
    car_brand_list = []
    if response_from_sqs:
        brand = event['Records'][0]["messageAttributes"]['brand']["stringValue"]
        type = event['Records'][0]["messageAttributes"]['type']["stringValue"]
        mile = event['Records'][0]["messageAttributes"]['mile']["stringValue"]
        year = event['Records'][0]["messageAttributes"]['Year']["stringValue"]
        email = event['Records'][0]["messageAttributes"]['Email']["stringValue"]
        
        
        car_brand_list.append(brand.title())
        
        car_id_list = query_car(car_brand_list)
        if not car_id_list:
            message = "Sorry, we could not recommend the related car based on your information. Please use our manual search. Have a good one!"
        else:
            owner_email = ""
            
            for car_id in car_id_list:
                response_from_DB = table.query(
                    KeyConditionExpression=Key('car_id').eq(car_id)
                    )
                print("DB repsonse",response_from_DB)
                if response_from_DB['Items']:
                    model_DB = response_from_DB['Items'][0]["model"]
                    available_DB = response_from_DB['Items'][0]["is_available"]
                    year_DB = response_from_DB['Items'][0]["year"]
                    mile = response_from_DB['Items'][0]["miles"]
                    score = response_from_DB['Items'][0]["score"]
                    email = response_from_DB['Items'][0]["owner"]
                    if model_DB == type and available_DB and abs(int(year_DB) - int(year))<=5 and abs(int(mile)-int(mile))<=5000 and float(score)>=3.5 :
                        owner_email = email 
                        break
            if not owner_email:
                message = "Sorry, we could not recommend the related car based on your information. Please use our manual search. Have a good one!"
            else:
                message = "This is our recommendation, which we think it is the best. The Dealer email is "+str(owner_email)
        
        send_email(email, message)
        
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=event['Records'][0]['receiptHandle']
        )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
            },
            'body': json.dumps({'results': message})
        }
    else:
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
            },
            'body': json.dumps("SQS queue is now empty")
        }


def query_car(brands):
    query = {
        "size":50,
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
        return []
    
def send_email(email, body_text):
    
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "ez2347@columbia.edu"
    
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = email
    
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    #CONFIGURATION_SET = "ConfigSet"
    
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"
    
    # The subject line for the email.
    SUBJECT = "Car Recommendation Based On your Given Information"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (body_text)
                
    # The HTML body of the email.
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
                    cred.secret_key,
                    region,
                    service,
                    session_token=cred.token)
