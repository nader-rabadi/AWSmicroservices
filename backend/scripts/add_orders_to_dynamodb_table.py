import boto3
import json

try:

    # Create a session
    session = boto3.session.Session()

    # Get the current AWS region. AWS region was set when
    # I ran 'aws configure' to setup my local environemnt.
    aws_region = session.region_name
    if aws_region is None:
        raise ValueError('Invalid AWS region')
    print(f'aws_region: {aws_region}')
    
    dynamodb = boto3.resource('dynamodb',  region_name=aws_region)

    table = dynamodb.Table('Orders')

    with open('orders.json') as json_file:
        orders_list = json.load(json_file)
    
    # Add to the table all items from the json file
    for order in orders_list:
        table.put_item(Item=order)

except (Exception, ValueError) as error:
    print(f'Exception error: add_orders_to_dynamodb_table : {error}')

else:
    # If no errors are detected, continue to execute the following:
    print(f'else block: add_orders_to_dynamodb_table :')
    print(f'Orders added successfully.')

finally:
    # Execute the following code whether or not an exception has been raised:
    print(f'finally block: add_orders_to_dynamodb_table :')

