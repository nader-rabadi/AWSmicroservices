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

class TestGeneratePresignedURL(unittest.TestCase):

    @mock_aws
    def setUp(self):

        os.environ['REPORTS_BUCKET'] = 'test_bucket'
        
        # Import after patching env variables
        from handlers.generate_presigned_url.generate_presigned_url import generate_presigned_url
        from handlers.generate_presigned_url.generate_presigned_url import s3

        self.generate_presigned_url = generate_presigned_url  # Store it in an instance variable
        self.s3 = s3

    def tearDown(self):
        os.environ.pop('REPORTS_BUCKET', None)

    @patch('handlers.generate_presigned_url.generate_presigned_url.s3.generate_presigned_url')
    @mock_aws
    def test_generate_presigned_url_success(self, mock_generate_presigned_url):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')        

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in the AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource
        patch_client(self.s3)

        bucket_name = os.environ['REPORTS_BUCKET']
        bucket_object = 'test-object'

        self.s3.create_bucket(
            Bucket=bucket_name
        )

        self.s3.put_object(
            Bucket=bucket_name,
            Key=bucket_object,
            Body='test data'
        )

        mock_generate_presigned_url.return_value = "https://mock-presigned-url.com"

        valerror = {}
        bucket_name = bucket_name
        object_name = bucket_object
        expiration_in_seconds = 3600
        key_name = 'presigned_url_key'
        
        # Call the function under test
        result = self.generate_presigned_url(bucket_name, object_name, expiration_in_seconds, key_name, valerror)

        # Assert the result
        self.assertEqual(result, {'presigned_url_key': 'https://mock-presigned-url.com'})
        self.assertEqual(valerror, {})  # Ensure valerror is not modified

    @patch('handlers.generate_presigned_url.generate_presigned_url.s3.generate_presigned_url')
    @mock_aws
    def test_generate_presigned_url_failure(self, mock_generate_presigned_url):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')        

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in the AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource
        patch_client(self.s3)

        bucket_name = os.environ['REPORTS_BUCKET']
        bucket_object = 'test-object'

        self.s3.create_bucket(
            Bucket=bucket_name
        )

        self.s3.put_object(
            Bucket=bucket_name,
            Key=bucket_object,
            Body='test data'
        )

        mock_generate_presigned_url.return_value = None

        valerror = {}
        bucket_name = bucket_name
        object_name = bucket_object
        expiration_in_seconds = 3600
        key_name = 'presigned_url_key'
        
        # Call the function under test
        result = self.generate_presigned_url(bucket_name, object_name, expiration_in_seconds, key_name, valerror)

        # Assert the result
        self.assertIsNone(result)
        self.assertIn('error', valerror)

    @patch('handlers.generate_presigned_url.generate_presigned_url.s3.generate_presigned_url')
    @mock_aws
    def test_generate_presigned_url_empty_string(self, mock_generate_presigned_url):
        print(f'***************************************************')
        print(f'Unit Test: {self.__class__.__name__} : {self._testMethodName} :')
        print(f'***************************************************')        

        # https://docs.getmoto.org/en/latest/docs/getting_started.html
        # According to moto documentation, I can use the clients and resources that I created
        # in the AWS Lambda function, and then patch them (using patch_client() and patch_resource())
        # to be used with moto.
        from moto.core import patch_client, patch_resource
        patch_client(self.s3)

        bucket_name = os.environ['REPORTS_BUCKET']
        bucket_object = 'test-object'

        self.s3.create_bucket(
            Bucket=bucket_name
        )

        self.s3.put_object(
            Bucket=bucket_name,
            Key=bucket_object,
            Body='test data'
        )

        mock_generate_presigned_url.return_value = ''

        valerror = {}
        bucket_name = bucket_name
        object_name = bucket_object
        expiration_in_seconds = 3600
        key_name = 'presigned_url_key'
        
        # Call the function under test
        result = self.generate_presigned_url(bucket_name, object_name, expiration_in_seconds, key_name, valerror)

        # Assert the result
        self.assertIsNone(result)
        self.assertIn('error', valerror)

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