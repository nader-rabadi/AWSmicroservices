import json
import boto3
import os

frontend_url = os.environ['FRONTEND_URL']
state_machine_arn = os.environ['STATE_MACHINE_ARN']
client = boto3.client('stepfunctions') # SFN in boto3 documentation

def run_state_machine(input_data, valerror):
    """
    This functions starts the execution of a state machine, and immediately
    returns with the ARN of the state machine's execution.

    Parameters:

    input_data: Order data which includes customer info and order info
    valerror: returned exception error

    Returns:

    State Machine's execution ARN

    """

    ret = ''

    try:
        # Start the state machine execution
        # The response is a dictionary that contains the ARN that identifies the execution,
        #  and the date the execution is started.
        response = client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input_data)  # Convert the dictionary to JSON string
        )

        print(f'response: {response}')

        run_arn = response['executionArn']
        
        ret = run_arn

    except (Exception, ValueError) as error:
        print(f'Exception error: run_state_machine : {error}')
        valerror['error'] = error

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: run_state_machine :')

    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: run_state_machine :')

    return ret

def lambda_handler(event, context):

    print(f'event (before starting state machine): {event}')
    
    input_data = {
        'body': event['body']  # event['body'] is already a JSON string
    }

    body = json.dumps({'message': 'Order accepted successfully'})

    httpret = {
        'statusCode': 202,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': frontend_url,
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Credentials': True,
            'Content-Type': 'application/json'
        },
        'body': body
    }

    ret = httpret

    try:
        valerror = {'error':''}
        response = run_state_machine(input_data, valerror)
        httpret['body'] = json.dumps({'executionArn':response})

    except Exception as error:
        print(f'Exception error: {error}')
        httpret['statusCode'] = 500
        httpret['body'] = json.dumps({'error': str(error)})
        ret = httpret
    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: do nothing for now')
        
        ret = httpret
    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: do nothing for now')

    return ret    
