import os
import boto3
import json
from datetime import datetime
import html

s3_bucket_name = os.environ['REPORTS_BUCKET']
s3 = boto3.client('s3')

def write_report(html_str):    
    params = {
        'Bucket': s3_bucket_name,
        'Key': 'productreport.html',
        'Body': html_str.encode(),
        'CacheControl': 'max-age=0',
        'ContentType': 'text/html'
    }

    s3.put_object(**params)

def create_html_products(products, valerror):
    """
    This function create an html string that contains information
    about products.

    Parameters:

    products: List of products
    valerror: returned exception error

    Returns:

    HTML string. Otherwise, None.
    
    """

    ret = None

    try:
        html_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Products Report</title>
                <style>
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }
                    th, td {
                        text-align: left;
                        padding: 8px;
                        border-bottom: 1px solid #ddd;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
        </head>
        <body>
            <h1>List of Products</h1>
                <table>
                    <tr>
                        <th>Product ID</th>                        
                        <th>Product Name</th>
                        <th>Price</th>
                        <th>Available</th>
                    </tr>
        """

        for product in products:
            id = product['id']            
            product_name = product['product_name']
            price = product['price']
            inventory_count = product['inventory_count']
            
            html_str += f"""
            <tr>
                <td>{id}</td>                
                <td>{product_name}</td>
                <td>{price}</td>
                <td>{inventory_count}</td>
            </tr>
            """
        html_str += """
            </table>
        </body>
        </html>
        """

        html_str = html_str.replace("\n", "")

        ret = html_str

    except Exception as error:
        print(f'Exception error: {error}')

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: do nothing for now')
        
    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: do nothing for now')

    return ret

def lambda_handler(event, context):

    print(f'event: {event}')
    ret = False

    try:        
        valerror = {'error':''}
        # see template yaml: ResultPath: '$.productsDataResult'
        html_products = create_html_products(event['productsDataResult']['products'], valerror)
        if html_products is None:
            raise ValueError(f'Could not create html for products')
        
        write_report(html_products)

        ret = True

    except Exception as error:
        print(f'Exception error: {error}')

    else:
        # If no errors are detected, continue to execute the following:
        print(f'else block: do nothing for now')
        
    finally:
        # Execute the following code whether or not an exception has been raised:
        print(f'finally block: do nothing for now')

    return ret

