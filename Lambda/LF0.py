import json
import boto3

client = boto3.client('lexv2-runtime')

def lambda_handler(event, context):
    print(f'input event is {event}')
    # handle prior OPTIONS requests
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': ''
        }
    
    msg_from_user = json.loads(event["body"])["messages"][0]["unstructured"]["text"]
    print(f"Message from frontend: {msg_from_user}")

    if msg_from_user:
        response = client.recognize_text(
            botId='WVIDOLLPX5', # MODIFY HERE
            botAliasId='TSTALIASID', # MODIFY HERE
            localeId='en_US',
            sessionId='testuser',
            text=msg_from_user
        )
        res = response['messages'][0]['content']
    else:
        res = 'Please try again.'
    print(f'Message from Chatbot: {res}')
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps({
            'messages': [{
                'type': 'unstructured',
                'unstructured': {
                    'text': res
                }
            }]
        })
    }
