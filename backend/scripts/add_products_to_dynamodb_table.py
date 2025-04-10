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

    table = dynamodb.Table('Products')

    with open('products.json') as json_file:
        products_list = json.load(json_file)
    
    # Add to the table all items from the json file
    for product in products_list:
        table.put_item(Item=product)

except (Exception, ValueError) as error:
    print(f'Exception error: add_products_to_dynamodb_table : {error}')

else:
    # If no errors are detected, continue to execute the following:
    print(f'else block: add_products_to_dynamodb_table :')
    print(f'Orders added successfully.')

finally:
    # Execute the following code whether or not an exception has been raised:
    print(f'finally block: add_products_to_dynamodb_table :')

