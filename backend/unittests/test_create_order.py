import unittest
from unittest.mock import patch, Mock
import json
import os
import sys
from moto import mock_aws

# Append the path to sys.path, in order to import from DocumentLambdaFunction/
path_to_add = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path_to_add)

class TestCreateOrder(unittest.TestCase):

    def setUp(self):

        os.environ['STATE_MACHINE_ARN'] = 'test_state_machine'
        os.environ['FRONTEND_URL'] = 'test_frontend_url'
        
        # Import after patching env variables
        from handlers.create_order.create_order import run_state_machine
        from handlers.create_order.create_order import client

        self.run_state_machine = run_state_machine  # Store it in an instance variable
        self.client = client

    def tearDown(self):
        os.environ.pop('STATE_MACHINE_ARN', None) 
        os.environ.pop('FRONTEND_URL', None)    

    @patch('handlers.create_order.create_order.client.start_execution')
    @mock_aws
    def test_run_state_machine_success(self, mock_start_execution):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in the AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource
        patch_client(self.client)

        executionArn = 'arn:aws:states:region:123456789012:execution:stateMachineName:executionId'

        mock_start_execution.return_value = {
            'executionArn': executionArn
        }

        valerror = {}
        input_data = {'key': 'value'}

        # Call the function under test
        result = self.run_state_machine(input_data, valerror)

        self.assertEqual(result, executionArn)

    @patch('handlers.create_order.create_order.client.start_execution')
    @mock_aws
    def test_run_state_machine_failure(self, mock_start_execution):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in the AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource
        patch_client(self.client)

        mock_start_execution.side_effect = Exception("State machine failed to start")

        valerror = {}
        input_data = {'key': 'value'}

        # Call the function under test
        result = self.run_state_machine(input_data, valerror)

        # Assert that the result is '' (error status)
        self.assertEqual(result, '')
        # Assert that valerror contains the exception
        self.assertTrue('error' in valerror)
        self.assertEqual(str(valerror['error']), "State machine failed to start")

    @patch('handlers.create_order.create_order.client.start_execution')
    @mock_aws
    def test_run_state_machine_value_error(self, mock_start_execution):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in the AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource
        patch_client(self.client)

        mock_start_execution.side_effect = ValueError("Invalid input")

        valerror = {}
        input_data = {'key': 'value'}

        # Call the function under test
        result = self.run_state_machine(input_data, valerror)

        # Assert that the result is '' (error status)
        self.assertEqual(result, '')
        # Assert that valerror contains the exception
        self.assertTrue('error' in valerror)
        self.assertEqual(str(valerror['error']), "Invalid input")

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
