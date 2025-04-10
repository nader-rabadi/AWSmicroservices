import os
import boto3
import json

frontend_url = os.environ['FRONTEND_URL']
aws_region_name = os.environ['AWS_REGION']
ddb_table_name = os.environ['ORDERS_TABLE']
dynamodb = boto3.resource('dynamodb', region_name=aws_region_name)

def get_order_from_ddb(table_name, order_id, valerror):
    """
    This function gets an order from DynamoDB table

    Parameters:

    table_name: Name of the DynamoDB Table that has orders
    order_id: Table key, which is also used to identify an order
    valerror: returned exception error

    Returns:

    Order dict. Otherwise, None.
    
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

        response = ddb_table.get_item(
            Key={'id': order_id}
        )

        if 'Item' in response:
            print(f'response: {response}')
            order = response['Item']
            print(f'order: {order}')
        else:
            order = {'message': f'Order {order_id} not found'}
            print(f'order: {order}')

    except (Exception, ValueError) as error:
        print(f'Exception error: get_order_from_ddb : {error}')
        valerror['error'] = error

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: get_order_from_ddb :')

        ret = order

    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: get_order_from_ddb :')

    return ret


def lambda_handler(event, context):
    body = json.dumps([])

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
        # API Gateway sends a message to Lambda function that includes
        # 'pathParameters'. In this key, there is the requested item 'id'.
        id = event['pathParameters']['id']
        
        valerror = {'error':''}
        order = get_order_from_ddb(ddb_table_name, id, valerror)

        if order is not None and 'message' in order and 'not found' in order['message']:
            raise ValueError(order['message'])
        else:
            body = json.dumps(order)

        httpret['body'] = body

    except (Exception, ValueError) as error:
        print(f'Exception error: {error}')        
        if order is not None and 'message' in order and str(error) == order['message']:
            httpret['statusCode'] = 404
        else:
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
