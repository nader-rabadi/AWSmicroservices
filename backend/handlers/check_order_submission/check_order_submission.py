import json
import boto3
import os

frontend_url = os.environ['FRONTEND_URL']
client = boto3.client('stepfunctions') # SFN in boto3 documentation

def check_submission_status(arn, valerror):
    """
    This functions returns the status of a state machine's execution

    Parameters:

    arn: Execution ARN of a state machine
    valerror: returned exception error

    Returns:

    Status

    """

    ret = ''

    try:
        response = client.describe_execution(
            executionArn = arn,
            includedData='ALL_DATA'
            )
            
        status = response['status']

        ret = status

    except (Exception, ValueError) as error:
        print(f'Exception error: check_submission_status : {error}')
        valerror['error'] = error

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: check_submission_status :')

    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: check_submission_status :')

    return ret

def lambda_handler(event, context):

    print(f'event (before starting state machine): {event}')

    execution_arn = event['pathParameters']['executionArn']

    body = json.dumps({'message': 'Order created successfully'})

    httpret = {
        'statusCode': 200,
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
        response = check_submission_status(execution_arn, valerror)
        httpret['body'] = json.dumps({'status':response})

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
