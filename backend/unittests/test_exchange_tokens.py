import unittest
from unittest.mock import patch, Mock
import json
import os
import sys

# Append the path to sys.path, in order to import from DocumentLambdaFunction/
path_to_add = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path_to_add)

class TestAuthorizationToTokens(unittest.TestCase):

    def setUp(self):

        os.environ['FRONTEND_URL'] = 'test_frontend_url'
        
        # Import after patching env variables
        from handlers.exchange_tokens.exchange_tokens import authorization_to_tokens

        self.authorization_to_tokens = authorization_to_tokens  # Store it in an instance variable

    def tearDown(self):
        os.environ.pop('FRONTEND_URL', None) 

    @patch('handlers.exchange_tokens.exchange_tokens.requests.post')
    def test_authorization_to_tokens_success(self, mock_post):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')

        # Mock the response from requests.post
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'fake_access_token',
            'id_token': 'fake_id_token',
            'refresh_token': 'fake_refresh_token'
        }
        mock_post.return_value = mock_response

        # Define inputs for the function
        authorization_code = 'fake_authorization_code'
        code_verifier = 'fake_code_verifier'
        valerror = {}

        # Call the function
        result = self.authorization_to_tokens(authorization_code, code_verifier, valerror)

        # Assert that the status code is 200
        self.assertEqual(result['statusCode'], 200)

        # Assert that the body contains the expected tokens
        expected_body = {
            'access_token': 'fake_access_token',
            'id_token': 'fake_id_token',
            'refresh_token': 'fake_refresh_token'
        }
        self.assertEqual(json.loads(result['body']), expected_body)

    @patch('handlers.exchange_tokens.exchange_tokens.requests.post')
    def test_authorization_to_tokens_failure(self, mock_post):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')

        # Mock the response from requests.post for a failure case
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'invalid_grant'}
        mock_post.return_value = mock_response

        # Define inputs for the function
        authorization_code = 'fake_authorization_code'
        code_verifier = 'fake_code_verifier'
        valerror = {}

        # Call the function
        result = self.authorization_to_tokens(authorization_code, code_verifier, valerror)

        # Assert that the status code is 400 (failure case)
        self.assertEqual(result['statusCode'], 400)

        # Assert that the body contains the error message
        expected_body = {
            'error': 'Failed to exchange authorization code for tokens',
            'details': {'error': 'invalid_grant'}
        }
        self.assertEqual(json.loads(result['body']), expected_body)

    @patch('handlers.exchange_tokens.exchange_tokens.requests.post')
    def test_authorization_to_tokens_exception(self, mock_post):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')

        # Mock the exception raised by requests.post
        mock_post.side_effect = Exception('Network error')

        # Define inputs for the function
        authorization_code = 'fake_authorization_code'
        code_verifier = 'fake_code_verifier'
        valerror = {}

        # Call the function
        result = self.authorization_to_tokens(authorization_code, code_verifier, valerror)

        # Assert that the status code is 500 (error case)
        self.assertEqual(result['statusCode'], 500)

        # Assert that the body contains the error message
        expected_body = {
            'error': 'An error occurred while exchanging the authorization code',
            'details': 'Network error'
        }
        self.assertEqual(json.loads(result['body']), expected_body)

if __name__ == '__main__':
    unittest.main()
