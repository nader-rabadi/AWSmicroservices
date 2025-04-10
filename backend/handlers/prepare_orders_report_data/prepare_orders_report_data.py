import boto3
import os

aws_region_name = os.environ['AWS_REGION']
ddb_orders_table_name = os.environ['ORDERS_TABLE']
dynamodb = boto3.resource('dynamodb', region_name=aws_region_name)

def get_data_from_ddb(table_name, valerror):
    """
    This function gets data from DynamoDB table

    Parameters:

    table_name: Name of the DynamoDB Table that has data
    valerror: returned exception error

    Returns:

    List. Otherwise, None.
    
    """

    ret = None
    try:
        
        # From Boto3 documentation:
        # Instantiate a table resource object without actually creating a DynamoDB table.
        ddb_table = dynamodb.Table(table_name)       
        if 'not found' in ddb_table.table_status:
            # Boto3 documenation: the attributes (such as table_status) are lazy-loaded,
            # which means that these are not fetched immediately when the object is created.
            # So, once I call ddb_table.table_status, its value will be fetched.
            # If its value has an error exception, then the exception automatically occurs
            # before even executing the following line of code:
            raise ValueError(f'Table: {table_name} not found')
        print(f'ddb_table: {ddb_table}')

        response = ddb_table.scan()
        print(f'response: {response}')
        data = response['Items']
        print(f'data: {data}')

    except (Exception, ValueError) as error:
        print(f'Exception error: get_data_from_ddb : {error}')
        valerror['error'] = error

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: get_data_from_ddb :')

        ret = data

    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: get_data_from_ddb :')

    return ret

def lambda_handler(event, context):
            
    ret = None

    try:        
        valerror = {'error':''}
        orders = get_data_from_ddb(ddb_orders_table_name, valerror)
        if orders is None:
            raise ValueError(f'Could not get data from orders table')
        
        ret = {'orders':orders}

    except Exception as error:
        print(f'Exception error: {error}')

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: do nothing for now')
        
    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: do nothing for now')

    return ret
    
