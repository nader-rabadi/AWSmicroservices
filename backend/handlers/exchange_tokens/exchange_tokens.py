import json
import requests
import os

frontend_url = os.environ['FRONTEND_URL']

# AWS Cognito details
REDIRECT_URI = frontend_url+'/callback'  # The redirect URI configured in Cognito
TOKEN_URL = 'https://us-east-1khfrrcsq8.auth.us-east-1.amazoncognito.com/oauth2/token'
CLIENT_ID = '2ea9l3thndcatnjua0mc848s29'
# Use the following (instead of the above) if AWS Cognito resource works using SAM template.yaml:
#TOKEN_URL = os.environ['COGNITO_DOMAIN'] + '/oauth2/token'
#CLIENT_ID = os.environ['USER_POOL_CLIENT_ID']

def authorization_to_tokens(authorization_code, code_verifier, valerror):
    """
    This function sends a POST request to Cognito to exchange the authorization code
    with an access token

    Parameters:

    authorization_code = The authorization code that was received in the URL by the frontend
    code_verifier: The code verifier generated on the frontend

    Returns:

    Access token, ID token and Refresh token.
    
    """
   
    # Prepare the body for the token request
    token_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'code_verifier': code_verifier
    }
    
    print(f'token_data:{token_data}')

    # URL-encode the parameters
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
    }

    ret = {
        'statusCode': 200,
        'body': ''
    }
    
    try:
        # Send the POST request to the Cognito token endpoint
        response = requests.post(TOKEN_URL, data=token_data, headers=headers)

        print(f'response: {response.text}')
        ret['statusCode'] = response.status_code

        if response.status_code == 200:            
            ret['body'] = json.dumps(response.json())            
        else:
            ret['body'] = json.dumps({'error': 'Failed to exchange authorization code for tokens', 'details': response.json()})
    
    except (Exception, ValueError) as error:
        print(f'Exception error: authorization_to_tokens : {error}')
        valerror['error'] = error

        ret['statusCode'] = 500
        ret['body'] = json.dumps({'error': 'An error occurred while exchanging the authorization code', 'details': str(error)})

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: authorization_to_tokens :')

    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: authorization_to_tokens :')

    return ret

def lambda_handler(event, context):

    httpret = {
        'statusCode': 200,
        'headers': {
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Origin': frontend_url,
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Credentials': True
        },
        'body': ''
    }

    ret = httpret

    print(f'event: {event}')

    try:
        # Extract "authorization code" and "code verifier" from the request body
        body = json.loads(event['body'])
        authorization_code = body['code']
        code_verifier = body['code_verifier']
        
        valerror = {'error':''}
        response = authorization_to_tokens(authorization_code, code_verifier, valerror)

        httpret['statusCode'] = response['statusCode']
        httpret['body'] = response['body']

    except Exception as error:
        print(f'Exception error: {error}')
        httpret['statusCode'] = 400
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


