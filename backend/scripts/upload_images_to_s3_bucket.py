import logging
import boto3
from botocore.exceptions import ClientError
import os

# This example is from Boto3 documentation, with some modifications
s3_client = boto3.client('s3')

def upload_file(file_name, bucket, folder, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param folder: folder-like name in the bucket
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Create the full object path (i.e., folder/object_name)
    s3_object_name = f"{folder}/{object_name}"

    # Upload the file    
    try:
        response = s3_client.upload_file(file_name, bucket, s3_object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == '__main__':

    try:

        # Get AWS account ID from AWS Security Token Service (STS).
        # The account ID will be used to define a bucket name.
        sts = boto3.client('sts')
        account_id = sts.get_caller_identity()["Account"]
        if account_id is None:
            raise ValueError('Invalid AWS Account ID')
        
        bucket_name = f'images-{account_id}'

        prefix_name = 'images'

        print(os.getcwd())

        files = [
            '.\\product-1-image.jpeg',
            '.\\product-2-image.jpeg',
            '.\\product-3-image.jpeg',
            '.\\product-4-image.jpeg',
            '.\\company_logo.jpeg',
            '.\\event_banner.jpeg',
        ]
            

        for file in files:
            print(f"Uploading {file} to S3 bucket {bucket_name}...")
            upload_file(file, bucket_name, prefix_name)
            print(f"Upload of {file} successful!")
            
    except Exception as e:
        print(f"An error occurred while uploading {file}: {e}") 
