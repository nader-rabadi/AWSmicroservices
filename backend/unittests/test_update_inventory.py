import unittest
from unittest.mock import patch, Mock
import boto3
from moto import mock_aws
import os
import sys

# Append the path to sys.path, in order to import from DocumentLambdaFunction/
path_to_add = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path_to_add)

class TestUpdateInventory(unittest.TestCase):

    def setUp(self):

        os.environ['PRODUCTS_TABLE'] = 'test_table'
        
        # Import after patching env variables
        from handlers.update_inventory.update_inventory import update_inventory
        from handlers.update_inventory.update_inventory import dynamodb

        self.update_inventory = update_inventory  # Store it in an instance variable
        self.dynamodb = dynamodb

    def tearDown(self):
        os.environ.pop('PRODUCTS_TABLE', None) 

    @mock_aws
    def test_update_inventory(self):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource    
        patch_resource(self.dynamodb)

        # Setup mock DynamoDB
        table_name = os.environ['PRODUCTS_TABLE']

        ddb_table = self.dynamodb.Table(table_name) 

        # Create mock table
        self.dynamodb.create_table(
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

        # Adding some mock products to the table
        ddb_table.put_item(
            Item={
                'id': '1',
                'inventory_count': '10'
            }
        )
                
        valerror = {}
        received_order = {
            'customerproduct': {
                'productsToSubmit': [
                    {'id': '1', 'quantity': '2'}
                ]
            }
        }
        result = self.update_inventory(received_order, valerror)

        # Check if the function returns True indicating success
        self.assertTrue(result)

        # Verify the inventory count was updated
        response = ddb_table.get_item(Key={'id': '1'})
        self.assertEqual(response['Item']['inventory_count'], '8')    

    @mock_aws
    def test_update_inventory_not_found(self):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')

        # Test case where the product is not found

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource    
        patch_resource(self.dynamodb)

        # Setup mock DynamoDB
        table_name = os.environ['PRODUCTS_TABLE']

        ddb_table = self.dynamodb.Table(table_name) 

        # Create mock table
        self.dynamodb.create_table(
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

        # Adding some mock products to the table
        ddb_table.put_item(
            Item={
                'id': '1',
                'inventory_count': '10'
            }
        )
        
        received_order = {
            'customerproduct': {
                'productsToSubmit': [
                    {'id': '2', 'quantity': '5'}
                ]
            }
        }
        valerror = {}

        result = self.update_inventory(received_order, valerror)

        # Check if the function returns False indicating failure
        self.assertFalse(result)
        self.assertIn('error', valerror)  # Error should be set in valerror

    @mock_aws
    def test_update_inventory_insufficient_stock(self):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource    
        patch_resource(self.dynamodb)

        # Setup mock DynamoDB
        table_name = os.environ['PRODUCTS_TABLE']

        ddb_table = self.dynamodb.Table(table_name) 

        # Create mock table
        self.dynamodb.create_table(
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

        # Adding some mock products to the table
        ddb_table.put_item(
            Item={
                'id': '1',
                'inventory_count': '10'
            }
        )
        
        received_order = {
            'customerproduct': {
                'productsToSubmit': [
                    {'id': '1', 'quantity': '15'}
                ]
            }
        }
        valerror = {}

        result = self.update_inventory(received_order, valerror)

        # Check if the function returns False indicating failure
        self.assertFalse(result)
        self.assertIn('error', valerror)  # Error should be set in valerror

    @patch('handlers.update_inventory.update_inventory.dynamodb.Table')
    @mock_aws
    def test_update_inventory_insufficient_stock(self, mock_dynamodb_table):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource    
        patch_resource(self.dynamodb)

        mock_dynamodb_table.return_value.table_status = 'not found'
        
        received_order = {
            'customerproduct': {
                'productsToSubmit': [
                    {'id': '1', 'quantity': '15'}
                ]
            }
        }
        valerror = {}

        result = self.update_inventory(received_order, valerror)

        # Check if the function returns False indicating failure
        self.assertFalse(result)
        self.assertIn('error', valerror)  # Error should be set in valerror

if __name__ == '__main__':

    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    os.environ['AWS_REGION'] = 'us-east-1'

    unittest.main()

    #Remove the same path from sys.path when finished testing
    if path_to_add in sys.path:
        sys.path.remove(path_to_add)
