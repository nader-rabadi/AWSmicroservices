import os
import boto3
import json

frontend_url = os.environ['FRONTEND_URL']
aws_region_name = os.environ['AWS_REGION']
ddb_table_name = os.environ['PRODUCTS_TABLE']
dynamodb = boto3.resource('dynamodb', region_name=aws_region_name)

def get_products_from_ddb(table_name, valerror):
    """
    This function gets all products from DynamoDB table

    Parameters:

    table_name: Name of the DynamoDB Table that has the products
    valerror: returned exception error

    Returns:

    Products list. Otherwise, None.
    
    """

    ret = None
    try:
        
        # From Boto3 documentation:
        # Instantiate a table resource object without actually creating a DynamoDB table.
        ddb_table = dynamodb.Table(table_name)        
        if 'not found' in ddb_table.table_status:
            # Boto3 documenation: the attributes (such as table_status) are lazy-loaded,
            # which means that these are not fetched immediately when the object is created.
            # So, once I call ddb_table.table_status, its value will be fetched.
            # If its value has an error exception, then the exception automatically occurs
            # before even executing the following line of code:
            raise ValueError(f'Table: {table_name} not found')
        print(f'ddb_table: {ddb_table}')

        response = ddb_table.scan()
        print(f'response: {response}')
        products = response['Items']
        print(f'products: {products}')

    except (Exception, ValueError) as error:
        print(f'Exception error: get_products_from_ddb : {error}')
        valerror['error'] = error

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: get_products_from_ddb :')

        ret = products

    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: get_products_from_ddb :')

    return ret


def lambda_handler(event, context):
    body = json.dumps({
        'products': []
    })

    httpret = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,HEAD,OPTIONS',
            'Access-Control-Allow-Origin': frontend_url,
            'Access-Control-Allow-Credentials': True
        },
        'body': body
    }

    ret = httpret

    try:
        
        valerror = {'error':''}
        products = get_products_from_ddb(ddb_table_name, valerror)

        body = json.dumps({
        'products': products
        })

        httpret['body'] = body

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
