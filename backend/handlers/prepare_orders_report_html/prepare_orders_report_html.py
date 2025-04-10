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
        'Key': 'orderreport.html',
        'Body': html_str.encode(),
        'CacheControl': 'max-age=0',
        'ContentType': 'text/html'
    }

    s3.put_object(**params)

def create_html_orders(orders, valerror):
    """
    This function create an html string that contains information
    about orders.

    Parameters:

    orders: List of orders
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
            <title>Orders Report</title>
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
            <h1>List of Orders</h1>
                <table>
                    <tr>
                        <th>Order ID</th>                        
                        <th>Order Time</th>
                        <th>Total Amount</th>
                        <th>Products</th>
                    </tr>
        """

        for order in orders:
            order_id = order['id']            
            order_time = order['order_time']
            total_amount = order['total_amount']
            ordered_items = order['ordered_items']
            
            html_str += f"""
            <tr>
                <td>{order_id}</td>                
                <td>{order_time}</td>
                <td>{total_amount}</td>
                <td>
            """

            for product in ordered_items:
                id = product['product_id']
                product_name = product['product_name']
                quantity = product['quantity']
                amount = product['amount']

                html_str += f"""
                <div>
                    <p><strong>Product {id}:</string></p>
					    <ul>
						    <li><strong>Product Name:</strong> {product_name}</li>
						    <li><strong>Quantity Ordered:</strong> {quantity}</li>
						    <li><strong>Amount:</strong> {amount}</li>
					    </ul>
                </div>				
                """
            html_str += """
            </td>
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
    ret = None

    try:        
        valerror = {'error':''}
        # see template yaml: ResultPath: '$.ordersReportResult'
        html_orders = create_html_orders(event['ordersReportResult']['orders'], valerror)
        if html_orders is None:
            raise ValueError(f'Could not create html for orders')
        
        write_report(html_orders)

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

