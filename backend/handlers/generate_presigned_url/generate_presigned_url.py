import boto3
import os

EXPIRATION_IN_SECOND = 3600
s3_bucket_name = os.environ['REPORTS_BUCKET']
s3 = boto3.client('s3')

def generate_presigned_url(bucket_name, object_name, expiration_in_seconds, key_name, valerror):
    """
    This function calls Amazon S3 to generate and return a presigned URL for a given key.

    Parameters:
    
    bucket_name: S3 bucket name
    object_name: The object for which to generate a presigned URL
    expiration_in_seconds: The number of seconds for which the presigned URL is valid.
    key_name: A dictionary's key name to identify the URL.

    Returns:

    Dictionary whose key is key_name, and value is the presigned URL. Otherwise, None.

    """
    ret = None

    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration_in_seconds,
            HttpMethod='GET'
        )

        # It is not clear whether the return value from generate_presigned_url can be None or an empty string
        if presigned_url is None or presigned_url =="":
            raise ValueError("URL is not assigned")

        response = {key_name: presigned_url}
    
    except (Exception, ValueError) as error:
        print(f'Exception error: generate_presigned_url : {error}')
        valerror['error'] = error

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: generate_presigned_url :')

        ret = response

    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: generate_presigned_url :')

    return ret

def lambda_handler(event, context):

    bucket_name = s3_bucket_name

    ret = None

    try:
        object_name = "orderreport.html"
        expiration_in_seconds = EXPIRATION_IN_SECOND

        valerror = {'error':''}
        response_orders = generate_presigned_url(bucket_name,
                                                 object_name, 
                                                 expiration_in_seconds, 
                                                 'presigned_url_orders_str',
                                                 valerror)
        
        if response_orders is None:
            raise ValueError('Could not generate presigned URL for orders')

        object_name = "productreport.html"
        expiration_in_seconds = EXPIRATION_IN_SECOND

        valerror = {'error':''}
        response_products = generate_presigned_url(bucket_name,
                                                   object_name,
                                                   expiration_in_seconds,
                                                   'presigned_url_products_str',
                                                   valerror)
        
        if response_products is None:
            raise ValueError('Could not generate presigned URL for products')

        response = {'presigned_url_orders_str': response_orders, 'presigned_url_products_str': response_products}

    except (Exception, ValueError) as error:
        print(f'Exception error: {error}')        

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: do nothing for now')
        
        ret = response
    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: do nothing for now')

    return ret

