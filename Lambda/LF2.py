import json
import time
import os
#import logging
import boto3
import re
import datetime

#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)


# --- Helpers that build all of the responses ---

def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']

def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']
    return {}

def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        #logger.debug('resolvedValue={}'.format(slots[slotName]['value']['resolvedValues']))
        return slots[slotName]['value']['interpretedValue']
    else:
        return None

def elicit_slot(session_attributes, intent_request, slots, slot_to_elicit, slot_elicitation_style, message):
    return {'sessionState': {'dialogAction': {'type': 'ElicitSlot',
                                              'slotToElicit': slot_to_elicit,
                                              'slotElicitationStyle': slot_elicitation_style
                                              },
                             'intent': {'name': intent_request['sessionState']['intent']['name'],
                                        'slots': slots,
                                        'state': 'InProgress'
                                        },
                             'sessionAttributes': session_attributes,
                             'originatingRequestId': '2d3558dc-780b-422f-b9ec-7f6a1bd63f2e'
                             },
            'sessionId': intent_request['sessionId'],
            'messages': [ message ],
            'requestAttributes': intent_request['requestAttributes']
            if 'requestAttributes' in intent_request else None
            }

def build_validation_result(isvalid, violated_slot, slot_elicitation_style, message_content):
    return {'isValid': isvalid,
            'violatedSlot': violated_slot,
            'slotElicitationStyle': slot_elicitation_style,
            'message': {'contentType': 'PlainText', 
            'content': message_content}
            }

def validate_reservation(intent_request):
    
    brand = get_slot(intent_request, 'CarBrand')
    type = get_slot(intent_request, 'CarType')
    mile = get_slot(intent_request, 'CarMile')
    email = get_slot(intent_request, 'email')
    
    # valid car brand
    #if location and location.lower() not in valid_cities:
    #     return build_validation_result(False, 'Location', 'SpellByWord', 'Location is not valid in other city. Please enter a location in New York')
    
    
    #valid car type
    #if cuisine and cuisine.lower() not in cuisines:
    #    return build_validation_result(False,
    #                                    'cuisine',
    #                                   'SpellByWord',
    #                                   'This cuisine is not available') 
    
    '''
    valid mile
    if date:
        year, month, day = map(int, date.split('-'))
        date_to_check = datetime.date(year, month, day)
        if date_to_check < datetime.date.today():
            return build_validation_result(False,'date', 'SpellByWord','Please enter a valid Dining date')
    '''    
    if mile:
        try:
            mile = int(mile)
            if mile < 1 or mile > 1000:  # Adjust the range if needed
                return build_validation_result(False, 'CarMile', 'SpellByWord', 'Please enter a valid numeric CarMile value within the acceptable range (1-1000)')
        except ValueError:
            return build_validation_result(False, 'CarMile', 'SpellByWord', 'Please enter a valid numeric CarMile value')
        
    if email:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return build_validation_result(False, 'Email', 'SpellByWord', 'Your email address is invalid')
    
    
    return {'isValid': True}


def make_restaurant_reservation(intent_request):
    """
    Performs dialog management and fulfillment for checking an account
    with a postal code. Besides fulfillment, the implementation for this 
    intent demonstrates the following:
    1) Use of elicitSlot in slot validation and re-prompting.
    2) Use of sessionAttributes to pass information that can be used to
        guide a conversation.
    """
    print("Debug: Entered make_restaurant_reservation" )
    slots = get_slots(intent_request)
    brand = get_slot(intent_request, 'CarBrand')
    type = get_slot(intent_request, 'CarType')
    mile = get_slot(intent_request, 'CarMile')
    year = get_slot(intent_request, 'CarYear')
    email = get_slot(intent_request, 'Email')
    
    session_attributes = get_session_attributes(intent_request)
    
    
    
    if intent_request['invocationSource'] == 'DialogCodeHook':
        # Validate the slots. If any aren't valid, 
        # re-elicit for the value.
        validation_result = validate_reservation(intent_request)
        print("Debug: Validation result is: ", validation_result)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            
            return elicit_slot(
                session_attributes,
                intent_request,
                slots,
                validation_result['violatedSlot'],
                validation_result['slotElicitationStyle'],
                validation_result['message']
            )
        
    
    print(slots)
    if not brand or not type or not mile or not year or not email:
        return delegate(intent_request, slots)
    
    else:
        #sqs 
        sqs_client = boto3.client('sqs')
        queue_url = "https://sqs.us-east-1.amazonaws.com/061567209239/CarQueue"
        
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageAttributes={
                    'brand': {
                        'DataType': 'String',
                        'StringValue': brand
                    },
                    'type': {
                        'DataType': 'String',
                        'StringValue': type
                    },
                    'mile': {
                        'DataType': 'Number',
                        'StringValue': str(mile)
                    },
                    'Year': {
                        'DataType': 'String',
                        'StringValue': str(year)
                    },
                    'Email': {
                        'DataType': 'String',
                        'StringValue': email
                    }
                },
            MessageBody=('Information about user inputs of Dining Chatbot.'),
            )
        
        print("This is response, 11111111111111111")
        print("response", response)
        
        return close(
            intent_request,
            session_attributes,
            'Fulfilled',
            {'contentType': 'PlainText',
             'content': 'I have received your request. I will help you search car, and send the dealer information to you. Have a Great Day !!'
             }
        )
        
def delegate(intent_request, slots):
    return {
    "sessionState": {
        "dialogAction": {
            "type": "Delegate"
        },
        "intent": {
            "name": intent_request['sessionState']['intent']['name'],
            "slots": slots,
            "state": "ReadyForFulfillment"
        },
        'sessionId': intent_request['sessionId'],
        "requestAttributes": intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }
}
    
def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent'],
            'originatingRequestId': '2d3558dc-780b-422f-b9ec-7f6a1bd63f2e'
        },
        'messages': [ message ],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }

# --- Intents ---

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    intent_name = intent_request['sessionState']['intent']['name']
    response = None

    # Dispatch to your bot's intent handlers
    if intent_name == 'SearchingIntent':
        response = make_restaurant_reservation(intent_request)

    return response

# --- Main handler ---

def lambda_handler(event, context):
    """
    Route the incoming request based on the intent.

    The JSON body of the request is provided in the event slot.
    """

    # By default, treat the user request as coming from 
    # Eastern Standard Time.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    
    #logger.debug(f'event is {event}')
    response = dispatch(event)
    #logger.debug(f'response is {response}')
    
    return response
