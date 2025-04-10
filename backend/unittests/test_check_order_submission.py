import unittest
from unittest.mock import patch, Mock
import json
import os
import sys
from moto import mock_aws

# Append the path to sys.path, in order to import from DocumentLambdaFunction/
path_to_add = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path_to_add)

class TestCheckOrderSubmission(unittest.TestCase):

    def setUp(self):

        os.environ['FRONTEND_URL'] = 'test_frontend_url'
        
        # Import after patching env variables
        from handlers.check_order_submission.check_order_submission import check_submission_status
        from handlers.check_order_submission.check_order_submission import client

        self.check_order_submission = check_submission_status  # Store it in an instance variable
        self.client = client

    def tearDown(self):
        os.environ.pop('FRONTEND_URL', None)        


    @patch('handlers.check_order_submission.check_order_submission.client.describe_execution')
    @mock_aws
    def test_check_order_submission_success(self, mock_describe_execution):
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

        mock_describe_execution.return_value = {
            'status': "SUCCEEDED"
        }

        valerror = {}

        # Call the function under test
        result = self.check_order_submission(executionArn, valerror)

        self.assertEqual(result, "SUCCEEDED")

    @patch('handlers.check_order_submission.check_order_submission.client.describe_execution')
    @mock_aws
    def test_check_order_submission_failure(self, mock_describe_execution):
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

        mock_describe_execution.side_effect = Exception("State machine failed to start")

        valerror = {}

        # Call the function under test
        result = self.check_order_submission(executionArn, valerror)

        # Assert that the result is '' (error status)
        self.assertEqual(result, '')
        # Assert that valerror contains the exception
        self.assertTrue('error' in valerror)
        self.assertEqual(str(valerror['error']), "State machine failed to start")

    @patch('handlers.check_order_submission.check_order_submission.client.describe_execution')
    @mock_aws
    def test_check_order_submission_value_error(self, mock_describe_execution):
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

        mock_describe_execution.side_effect = ValueError("Invalid input")

        valerror = {}

        # Call the function under test
        result = self.check_order_submission(executionArn, valerror)

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
