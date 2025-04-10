import unittest
from unittest.mock import patch
import uuid
import os
import sys
from datetime import datetime
from moto import mock_aws

# Append the path to sys.path, in order to import from DocumentLambdaFunction/
path_to_add = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path_to_add)

class TestGenerateShortId(unittest.TestCase):

    def setUp(self):

        os.environ['ORDERS_TABLE'] = 'test_table'
        
        # Import after patching env variables
        from handlers.new_order.new_order import generate_short_id, MAX_LENGTH, ID_LENGTH

        self.generate_short_id = generate_short_id  # Store it in an instance variable
        self.ID_LENGTH = ID_LENGTH

    def tearDown(self):
        os.environ.pop('ORDERS_TABLE', None)

    @patch('uuid.uuid4')  # Mocking uuid4 to return a predictable UUID
    def test_generate_short_id_valid_length(self, mock_uuid):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')

        # Mock the UUID to return a known value
        mock_uuid.return_value = uuid.UUID('8b1a8c88-efa6-4925-b733-d40cfa6483c4')
        
        # Test for specific length
        result = self.generate_short_id(8)
        self.assertEqual(len(result), 8)
        self.assertTrue(result.isdigit())  # Check that it's numeric

    @patch('uuid.uuid4')
    def test_generate_short_id_max_length(self, mock_uuid):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')
                
        # Mock UUID
        mock_uuid.return_value = uuid.UUID('8b1a8c88-efa6-4925-b733-d40cfa6483c4')
        
        # Test for length greater than the max allowed
        result = self.generate_short_id(1000)
        self.assertEqual(len(result), self.ID_LENGTH)  # Check that it doesn't exceed max allowed length
        self.assertTrue(result.isdigit())  # Check that it's numeric

    @patch('uuid.uuid4')
    def test_generate_short_id_empty(self, mock_uuid):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')
                
        # Mock UUID
        mock_uuid.return_value = uuid.UUID('8b1a8c88-efa6-4925-b733-d40cfa6483c4')
        
        # Test for zero length
        result = self.generate_short_id(0)
        self.assertEqual(len(result), self.ID_LENGTH)  # Check the max allowed length
        self.assertTrue(result.isdigit())  # Check that it's numeric

    @patch('uuid.uuid4')
    def test_generate_short_id_empty(self, mock_uuid):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')
                
        # Mock UUID
        mock_uuid.return_value = uuid.UUID('8b1a8c88-efa6-4925-b733-d40cfa6483c4')
        
        # Test for -ve length
        result = self.generate_short_id(-2)
        self.assertEqual(len(result), self.ID_LENGTH)  # Check the max allowed length
        self.assertTrue(result.isdigit())  # Check that it's numeric        

    @patch('uuid.uuid4')
    def test_generate_short_id_numeric(self, mock_uuid):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')
                
        # Mock UUID
        mock_uuid.return_value = uuid.UUID('8b1a8c88-efa6-4925-b733-d40cfa6483c4')
        
        # Test for specific length, ensuring only numeric characters
        result = self.generate_short_id(6)
        self.assertEqual(len(result), 6)
        self.assertTrue(result.isdigit())  # Check that it's numeric

class TestCreateOrder(unittest.TestCase):

    def setUp(self):

        os.environ['ORDERS_TABLE'] = 'test_table'
        
        # Import after patching env variables
        from handlers.new_order.new_order import create_order

        self.create_order = create_order  # Store it in an instance variable

    def tearDown(self):
        os.environ.pop('ORDERS_TABLE', None)

    @patch('handlers.new_order.new_order.generate_short_id')  # Mocking generate_short_id
    @patch('handlers.new_order.new_order.datetime')  # Mocking datetime to return a fixed time
    def test_create_order_success(self, mock_datetime, mock_generate_short_id):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')
                
        # Set up mock return values
        mock_generate_short_id.return_value = '12345678'
        mock_datetime.now.return_value = datetime(2025, 4, 2, 12, 0, 0)
        
        # Sample input data (received order)
        received_order = {
            'personalInfo': {
                'customer_name': 'John Doe',
                'email': 'johndoe@example.com',
                'phone': '555-555-5555'
            },
            'customerproduct': {
                'productsToSubmit': [
                    {'id': 1, 'name': 'Product 1', 'quantity': 2, 'price': '10.00'},
                    {'id': 2, 'name': 'Product 2', 'quantity': 1, 'price': '20.00'}
                ]
            }
        }

        valerror = {'error':''}

        # Call the function with the test data
        result = self.create_order(received_order, valerror)

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], '12345678')
        self.assertEqual(result['customer_name'], 'John Doe')
        self.assertEqual(result['email'], 'johndoe@example.com')
        self.assertEqual(result['phone'], '555-555-5555')
        self.assertEqual(len(result['ordered_items']), 2)
        self.assertEqual(result['total_amount'], '40.00')
        self.assertEqual(result['order_time'], '2025-04-02T12:00:00Z')

    @patch('handlers.new_order.new_order.generate_short_id')
    def test_create_order_with_error(self, mock_generate_short_id):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')
                
        # Mock generate_short_id to raise an exception
        mock_generate_short_id.side_effect = ValueError("Invalid ID generation")

        # Sample input data (received order)
        received_order = {
            'personalInfo': {
                'customer_name': 'John Doe',
                'email': 'johndoe@example.com',
                'phone': '555-555-5555'
            },
            'customerproduct': {
                'productsToSubmit': [
                    {'id': 1, 'name': 'Product 1', 'quantity': 2, 'price': '10.00'}
                ]
            }
        }

        valerror = {'error':''}

        # Call the function with the test data
        result = self.create_order(received_order, valerror)

        # Assertions
        self.assertIsNone(result)
        self.assertIn('error', valerror)  # Check that an error is added to the valerror dict
        self.assertEqual(valerror['error'].args[0], 'Invalid ID generation')

    @patch('handlers.new_order.new_order.generate_short_id')
    def test_create_order_missing_key(self, mock_generate_short_id):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')
                
        # Mock generate_short_id to return a valid ID
        mock_generate_short_id.return_value = '12345678'

        # Sample input data (missing 'personalInfo' key)
        received_order = {
            'customerproduct': {
                'productsToSubmit': [
                    {'id': 1, 'name': 'Product 1', 'quantity': 2, 'price': '10.00'}
                ]
            }
        }

        valerror = {'error':''}

        # Call the function with the test data
        result = self.create_order(received_order, valerror)

        # Assertions
        self.assertIsNone(result)
        self.assertIn('error', valerror)  # Check that an error is added to the valerror dict
        self.assertTrue(isinstance(valerror['error'], KeyError))  # Check the error type KeyError due to the missing key in the dictionary

class TestPutItemInDynamoDB(unittest.TestCase):

    def setUp(self):

        os.environ['ORDERS_TABLE'] = 'test_table'
        
        # Import after patching env variables
        from handlers.new_order.new_order import put_item_in_dynamodb
        from handlers.new_order.new_order import dynamodb

        self.put_item_in_dynamodb = put_item_in_dynamodb  # Store it in an instance variable
        self.dynamodb = dynamodb

    def tearDown(self):
        os.environ.pop('ORDERS_TABLE', None)

    @mock_aws
    def test_put_item_in_dynamodb_success(self):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')
        

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in the AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource
        patch_resource(self.dynamodb)

        # Set up a mock DynamoDB table using moto        
        table_name = os.environ['ORDERS_TABLE']

        ddb_table = self.dynamodb.Table(table_name)

        table = self.dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'order_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'order_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        )
        
        # Sample order to insert
        order = {
            'order_id': '12345',
            'customer_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone': '555-555-5555',
            'ordered_items': [],
            'total_amount': '100.00'
        }

        ddb_response = {}
        valerror = {}

        # Call the function to test
        result = self.put_item_in_dynamodb(ddb_table, order, ddb_response, valerror)

        # Assertions
        self.assertTrue(result)  # The function should return True
        self.assertIn('ddb_response', ddb_response)  # Check if 'ddb_response' key exists
        self.assertEqual(ddb_response['ddb_response']['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertEqual(len(valerror), 0)  # No error should be in valerror

    @mock_aws
    def test_put_item_in_dynamodb_failure(self):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')
        
        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in the AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource
        patch_resource(self.dynamodb)        

        # Set up a mock DynamoDB table using moto        
        table_name = os.environ['ORDERS_TABLE']

        ddb_table = self.dynamodb.Table(table_name)

        table = self.dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'order_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'order_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        )
        
        # Sample order to insert with a wrong attribute (missing required key)
        order = {
            'customer_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone': '555-555-5555',
            'ordered_items': [],
            'total_amount': '100.00'
        }

        ddb_response = {}
        valerror = {}

        # Call the function to test
        result = self.put_item_in_dynamodb(ddb_table, order, ddb_response, valerror)

        # Assertions
        self.assertFalse(result)  # The function should return False in case of failure
        self.assertIn('error', valerror)  # Error should be in the valerror dict
        self.assertTrue(isinstance(valerror['error'], Exception))  # The error should be an instance of Exception

    @mock_aws
    def test_put_item_in_dynamodb_invalid_http_response(self):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')
        
        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in the AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource
        patch_resource(self.dynamodb)  

        table_name = os.environ['ORDERS_TABLE']

        ddb_table = self.dynamodb.Table(table_name)

        table = self.dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'order_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'order_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        )
        
        # Mock response for dynamodb.Table - indicating a None.
        dynamodb_mock_response = {'ResponseMetadata': {'HTTPStatusCode': 500}}

        # The moto library mocks AWS services, so you can return this response
        # when calling the `dynamodb.Table` method        
        ddb_table.put_item = lambda Item: dynamodb_mock_response

        order = {
            'order_id': '12345',
            'customer_name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone': '555-555-5555',
            'ordered_items': [],
            'total_amount': '100.00'
        }

        ddb_response = {}
        valerror = {}

        # Call the function to test
        result = self.put_item_in_dynamodb(ddb_table, order, ddb_response, valerror)

        # Assertions
        self.assertFalse(result)  # The function should return False if the HTTPStatusCode is not 200
        self.assertIn('error', valerror)  # Error should be in the valerror dict
        self.assertTrue(isinstance(valerror['error'], ValueError))  # Check if the error is ValueError

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
