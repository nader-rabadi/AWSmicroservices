import json
import boto3
import os

frontend_url = os.environ['FRONTEND_URL']
client = boto3.client('stepfunctions') # SFN in boto3 documentation

def get_presigned_urls_from_statemachine(arn, valerror):
    """
    This functions returns the presigned URLs from state machine's execution

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
            
        output = response['output']
        print(f'response: {response}')
        print(f'output: {output}')

        ret = output

    except (Exception, ValueError) as error:
        print(f'Exception error: get_presigned_urls_from_statemachine : {error}')
        valerror['error'] = error

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: get_presigned_urls_from_statemachine :')

    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: get_presigned_urls_from_statemachine :')

    return ret

def lambda_handler(event, context):

    print(f'event (before starting state machine): {event}')

    execution_arn = event['pathParameters']['executionArn']

    body = json.dumps({'message': 'Report created successfully'})

    httpret = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': frontend_url,
            'Access-Control-Allow-Methods': 'OPTIONS,GET',
            'Access-Control-Allow-Credentials': True,
            'Content-Type': 'application/json'
        },
        'body': body
    }

    ret = httpret

    try:
        valerror = {'error':''}
        response = get_presigned_urls_from_statemachine(execution_arn, valerror)
        httpret['body'] = json.dumps({'urloutputs':response})

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
