import os
import boto3
import json
import uuid
from datetime import datetime

ID_LENGTH = 8
MAX_LENGTH = 10
aws_region_name = os.environ['AWS_REGION']
ddb_table_name = os.environ['ORDERS_TABLE']
dynamodb = boto3.resource('dynamodb', region_name=aws_region_name)

def generate_short_id(length):
    """
    This function generates a UUID and returns a numeric value of size 'length'

    Parameters:

    length: Desirec length of the generated ID

    Returns:

    Base64 number of size 'length'
    """
    if length > MAX_LENGTH:
        length = ID_LENGTH

    if length <= 0:
        length = ID_LENGTH

    # Generate a UUID and take the first `length` characters of its hex representation
    unique_id = uuid.uuid4().hex[:length]

    # Convert the hex characters to numeric values
    numeric_id = ''.join(str(int(c, 16)) for c in unique_id)

    # Limit to length (in case conversion exceeds length characters)
    return numeric_id[:length]

def create_order(received_order, valerror):
    """
    This function creates a new order.

    Parameters:

    received_order: This is the order that the customer requested
    valerror: returned exception error

    Returns:

    order as a dict. Otherwise None

    """
    ret = None
    try:

        print(f'Received order is: {received_order}')

        # Generate a unique ID for this order
        unique_id = generate_short_id(ID_LENGTH)

        new_order = {}
        new_order['id'] = unique_id
        new_order['customer_name'] = received_order['personalInfo']['customer_name']
        new_order['email'] = received_order['personalInfo']['email']
        new_order['phone'] = received_order['personalInfo']['phone']
        new_order['ordered_items'] = []

        # Compute the total amount of ordered products
        total_amount = 0.0
        for product in received_order['customerproduct']['productsToSubmit']:
            # Compute from 'quantity' and 'price'
            product_amount = product['quantity'] * float(product['price'])
            total_amount += product_amount

            new_order['ordered_items'].append(
                {
                    "product_id": str(product['id']),
                    "product_name": product['name'],
                    "quantity": str(product['quantity']),
                    "amount": f"{product_amount:.2f}"
                }
            )
        
        new_order['total_amount'] = f"{total_amount:.2f}"
        new_order['order_time'] = datetime.now().isoformat() + "Z"

    except (Exception, ValueError) as error:
        print(f'Exception error: create_order : {error}')
        valerror['error'] = error

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: create_order :')

        ret = new_order

    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: create_order :')

    return ret

def put_item_in_dynamodb(dynamodb_table, order, ddb_response, valerror):
    """
    This function writes an order to DynamoDB

    Parameters:

    dynamodb_table: DynamoDB table
    order: This is the order that the customer requested 
    ddb_response: Returned response from DynamoDB    
    valerror: returned exception error

    Returns:

    True if operations are successful. Otherwise, False

    """
    ret = False
    try:

        ddb_response['ddb_response'] = dynamodb_table.put_item(Item=order)
        print(f'ddb response: {ddb_response['ddb_response']}')
        if ddb_response['ddb_response']['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise ValueError('Could not put DynamoDB Table item')
        
    except (Exception, ValueError) as error:
        print(f'Exception error: put_item_in_dynamodb : {error}')
        valerror['error'] = error

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: put_item_in_dynamodb :')

        ret = True

    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: put_item_in_dynamodb :')

    return ret

def lambda_handler(event, context):

    print(f'event (starting state machine): {event}')

    body = json.dumps([])

    ret = None

    try:
        # For POST request, get its body
        body = json.loads(event['body'])

        valerror = {'error':''}        
        order = create_order(body, valerror)
        if order is None:
            raise ValueError('Order creation failed!')
        print(f'new order: {order}')
        
        ddb_table = dynamodb.Table(ddb_table_name)
        if 'not found' in ddb_table.table_status:
            # Boto3 documenation: the attributes (such as table_status) are lazy-loaded,
            # which means that these are not fetched immediately when the object is created.
            # So, once I call ddb_table.table_status, its value will be fetched.
            # If its value has an error exception, then the exception automatically occurs
            # before even executing the following line of code:
            raise ValueError(f'Table: {ddb_table_name} not found')
        print(f'ddb_table: {ddb_table}')

        # Add the new order to DynamoDB table
        ddb_response = {'ddb_response':''}
        outcome = put_item_in_dynamodb(ddb_table, order, ddb_response, valerror)
        if outcome == False:
            raise ValueError('Error in put_item_in_dynamodb')
                
    except (Exception, ValueError) as error:
        print(f'Exception error: {error}')

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: do nothing for now')
        
        ret = {'order':body}
    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: do nothing for now')

    return ret
