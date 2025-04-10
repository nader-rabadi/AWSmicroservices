import os
import boto3
import json

aws_region_name = os.environ['AWS_REGION']
ddb_table_name = os.environ['PRODUCTS_TABLE']
dynamodb = boto3.resource('dynamodb', region_name=aws_region_name)

def update_inventory(received_order, valerror):
    """
    This function updates the inventory count for each ordered product.

    Parameters:

    received_order: This is the order that the customer requested
    valerror: returned exception error

    Returns:

    True if operations are successful. Otherwise, False

    """
    ret = False

    try:
                
        ddb_table = dynamodb.Table(ddb_table_name)
        if 'not found' in ddb_table.table_status:
            # Boto3 documenation: the attributes (such as table_status) are lazy-loaded,
            # which means that these are not fetched immediately when the object is created.
            # So, once I call ddb_table.table_status, its value will be fetched.
            # If its value has an error exception, then the exception automatically occurs
            # before even executing the following line of code:
            raise ValueError(f'Table: {ddb_table_name} not found')
        print(f'ddb_table: {ddb_table}')

        for product in received_order['customerproduct']['productsToSubmit']:
            product_quantity = int(product['quantity']) # This is a string. Convert to int
            product_id = product['id'] # This is a string

            print(f'product_quantity: {product_quantity}')
            print(f'product_id: {product_id}')

            # Get the product from DynamoDB
            response = ddb_table.get_item(Key={'id':product_id})

            if 'Item' not in response:
                raise ValueError(f'Product not found')
            
            item = response['Item']
            inventory_count = int(item['inventory_count'])

            if inventory_count < product_quantity:
                raise ValueError(f'Not enough stock available')
            
            print(f'inventory_count: {inventory_count}')

            new_val = str(inventory_count - product_quantity)

            response_update = ddb_table.update_item(
                Key={'id': product_id},
                UpdateExpression='SET inventory_count = :new_val',
                ExpressionAttributeValues={':new_val': new_val},
                ReturnValues='ALL_NEW'  # Return the updated item
            )

            # Until I find a way to store inventory_count as a Number without causing JSON serialization exception in Lambda
            # response_update = ddb_table.update_item(
            #     Key={'id': product_id},
            #     UpdateExpression='SET inventory_count = inventory_count - :product_quantity',
            #     ConditionExpression='inventory_count >= :product_quantity',  # Ensure stock is sufficient
            #     ExpressionAttributeValues={':product_quantity': product_quantity},
            #     ReturnValues='ALL_NEW'  # Return the updated item
            # )

            if 'Attributes' not in response_update:
                raise ValueError(f'Could not update inventory')
            
    except (Exception, ValueError) as error:
        print(f'Exception error: update_inventory : {error}')
        valerror['error'] = error

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: update_inventory :')

        ret = True

    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: update_inventory :')

    return ret

def lambda_handler(event, context):

    print(f'event (updating inventory via state machine): {event}')

    ret = False

    try:

        # Update inventory_count for each ordered product
        valerror = {'error':''}
        data = event['order']
        outcome = update_inventory(data, valerror)
        if outcome == False:
            raise ValueError('Error in update_inventory')
        
        ret = True

    except (Exception, ValueError) as error:
        print(f'Exception error: {error}')

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: do nothing for now')
        
    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: do nothing for now')

    return ret
