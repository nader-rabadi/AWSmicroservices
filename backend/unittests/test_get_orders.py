import unittest
from unittest.mock import patch
import boto3
import os
import sys
from moto import mock_aws
from botocore.exceptions import ClientError

# Append the path to sys.path, in order to import from DocumentLambdaFunction/
path_to_add = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path_to_add)

class TestGetOrdersFromDDB(unittest.TestCase):

    @mock_aws
    def setUp(self):

        os.environ['ORDERS_TABLE'] = 'test_table'
        os.environ['FRONTEND_URL'] = 'test_frontend_url'
        
        # Import after patching env variables
        from handlers.get_orders.get_orders import get_orders_from_ddb
        from handlers.get_orders.get_orders import dynamodb

        self.get_orders_from_ddb = get_orders_from_ddb  # Store it in an instance variable
        self.dynamodb = dynamodb

    def tearDown(self):
        os.environ.pop('ORDERS_TABLE', None)
        os.environ.pop('FRONTEND_URL', None) 

    @mock_aws
    def test_get_orders_from_ddb_success(self):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')        

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in the AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource
        patch_resource(self.dynamodb)

        get_orders_from_ddb = self.get_orders_from_ddb
        dynamodb = self.dynamodb

        # Setup mock DynamoDB
        table_name = os.environ['ORDERS_TABLE']

        ddb_table = dynamodb.Table(table_name) 

        # Create mock table
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

        # Adding some mock orders to the table
        ddb_table.put_item(
            Item={
                "id": "1",
                "customer_name": "Customer1",
                "email": "Customer1@email.com",
                "phone": "123456789",
                "total_amount": "17.00",
                "ordered_items": [
                    {
                        "product_id": "2",
                        "product_name": "Product2",
                        "quantity": "3",
                        "amount": "9.00"
                    },
                    {
                        "product_id": "4",
                        "product_name": "Product4",
                        "quantity": "2",
                        "amount": "8.00"
                    }
                ],        
                "order_time": "2025-03-12T13:11:51.761Z"
            }
        )
        ddb_table.put_item(
            Item={
                "id": "2",
                "customer_name": "Customer2",
                "email": "Customer2@email.com",
                "phone": "123456789",
                "total_amount": "6.00",
                "ordered_items": [
                    {
                        "product_id": "2",
                        "product_name": "Product2",
                        "quantity": "1",
                        "amount": "2.00"
                    },
                    {
                        "product_id": "4",
                        "product_name": "Product4",
                        "quantity": "1",
                        "amount": "4.00"
                    }
                ],        
                "order_time": "2025-01-12T13:11:51.761Z"
            }
        )

        # Prepare a valerror dictionary to capture errors
        valerror = {'error':''}

        # Call the function under test
        result = get_orders_from_ddb(table_name, valerror)

        # Check the result
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)  # We inserted two orders
        self.assertEqual(result[0]['id'], '1')  # First order's ID should be '1'
        self.assertEqual(result[1]['id'], '2')  # Second order's ID should be '2'
        self.assertEqual(valerror, {'error':''})  # No error should be set

    @mock_aws
    def test_get_orders_from_ddb_table_not_found(self):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')    

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in the AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource
        patch_resource(self.dynamodb)

        get_orders_from_ddb = self.get_orders_from_ddb
        dynamodb = self.dynamodb

        # Setup mock DynamoDB
        table_name = os.environ['ORDERS_TABLE']

        # Prepare a valerror dictionary to capture errors
        valerror = {'error':''}

        # Call the function under test
        result = get_orders_from_ddb(table_name, valerror)

        # Check the result
        self.assertIsNone(result)  # No orders should be returned
        self.assertIn('error', valerror)  # There should be an error captured in valerror    
        self.assertIn(f'Table: {table_name} not found', str(valerror['error'])) # error message is part of a long error message
    
if __name__ == '__main__':

    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    os.environ['AWS_REGION'] = 'us-east-1'
    
    unittest.main()
    
    # Remove the same path from sys.path when finished testing
    if path_to_add in sys.path:
        sys.path.remove(path_to_add)