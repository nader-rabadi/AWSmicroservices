
# Project Overview

This project is a web application for a fictional cookies company. I developed this project using React for the frontend and AWS for the backend. The application allows customers to browse the company’s product catalog, which includes details such as product name, price, image, and stock availability. Users can select the quantity of each product they wish to purchase and proceed to a checkout form to provide personal information for completing the purchase. Additionally, employees of the company can log into the company's internal resources through a sign-in feature. Once authenticated, employees can access a dashboard to view all customer orders, click on individual orders for detailed information, generate reports about products and orders, and sign out when done. This project integrates user interaction with secure employee functionality, offering a seamless experience for both customers and company staff.

# Project Objective

The objective of this project is to apply and enhance the knowledge I gained from a comprehensive AWS cloud services course: AWS Cloud Institute's Cloud Application Developer Track. This project is specifically focusing on the development of serverless microservices as the backend for a server-client web application. The AWS course provided hands-on, challenge-based labs experience teaching the fundamentals of using AWS services, in addition to building and managing the backend architecture, including:

- Amazon API Gateway
- AWS Lambda
- Amazon Cognito
- Amazon DynamoDB
- Amazon S3
- Amazon SNS
- AWS Step Functions
- AWS Serverless Application Model (SAM)

These serverless services were designed to function together to support a robust, scalable, and cost-effective backend infrastructure.

One of the labs primarily concentrated on AWS architecture and service development, providing foundational knowledge to integrate AWS backend components into a working solution. The focus was not on front-end development but rather on creating and deploying serverless applications, managing authentication, and configuring various services for communication between the front end and backend. As part of the course, I also learned the basics of React, Vite, and Axios to enable front-end communication with the AWS backend via the Amazon API Gateway.

The primary aim in this project is to demonstrate practical, real-world application of serverless AWS technologies in a full-stack environment, showcasing my ability to design and implement backend solutions while integrating them with a simple client-side interface.

# How to Deploy

This project assumes you had already installed and are familiar with using the following components in your development environment:
- Boto3 (in Python)
- AWS CLI
- AWS SAM
- npm
- React

This project also uses an additional library in React called pkce-challenge.

**Please read the notes in the next section before running the following commands:**

- Under `/backend/` folder, run from the terminal:
  - sam validate
  - sam build
  - sam deploy

- Under `/my-react-app/` folder, run from the terminal:
  - npm install
  - npm run dev


# Notes on Development Environment and on Amazon Cognito

- In the React code, I added a `Test Mode` feature to allow testing components that are otherwise only accessible to signed-in users of this fictional company. To disable `Test Mode`, in App.jsx change the following line of code from `true` to `false`:
```
const [isTestingUserSignedIn, setIsTestingUserSignedIn] = useState(true);
```
- In AWS SAM template.yaml, the following Amazon Cognito resources (CognitoUserPool, CognitoUserPoolClient, CognitoUserPoolDomain) will be created successfully when running 'sam deploy'. However, when I run my React application to test this Amazon Cognito resource, I get a response from it indicating: '403 Forbidden'. Until this issue is resolved, I manually created Amazon Cognito in AWS console, and then manually copy the Amazon Cognito Client ID and Domain for use in `ExchangeTokensLambda` AWS Lambda python code. So, the Amazon Cognito resource in template.yaml named `product_app` will be created but it will not be used. Furthermore, if you create Amazon Cognito resource manually, then make sure to select `Authorization code grant` as the OAuth grant types since I used this grant type in my Python code.

- In `/backend/handlers/exchange_tokens.py`, Replace **TOKEN_URL,** and **CLIENT_ID,** with your Amazon Cognito setup. If the issue of Amazon Cognito resource in SAM template.yaml is resolved, then set **TOKEN_URL** to the environment variable **COGNITO_DOMAIN**, and set **CLIENT_ID** to the environement variable **USER_POOL_CLIENT_ID**.

- In `/my-react-app/.env`,
  - Replace **VITE_COGNITO_AUTH_URL** and **VITE_CLIENT_ID** with your Amazon Cognito setup.
  - Replace **VITE_API_GATEWAY_URL** with your Amazon API Gateway URL.
  - Replace **VITE_PRODUCTS_IMAGES_BUCKET_URL** with your Amazon S3 images Bucket URL.

- For development testing, I use `React+Vite+Axios` and hence my local development URL is 'http://localhost:5173'. If this URL is different than the URL in your settings, then you will need to update the following:
  - **template.yaml**: `FrontendUrl` in `Parameters` section
  - **template.yaml**: `AllowOrigin` for `ProductAPI` resource
  - **samconfig.toml**: `FrontendUrl` in `parameter_overrides` section 
  - **/my-react-app/.env**: `VITE_REDIRECT_URI`

- In `/backend/scripts/`, there are three scripts to help you automate some tasks after deploying template.yaml resources:
  - **upload_images_to_s3_bucket.py**: This script uploads images, which are displayed in the frontend web application, to the `ImagesBucket` resource.
  - **add_products_to_dynamodb_table.py**: This script adds products information to the Amazon DynamoDB `ProductsTable` resource.
  - **add_orders_to_dynamodb_table.py**: If you want to preset your database with some orders (for testing purpose), then this script adds some orders information to the Amazon DynamoDB `OrdersTable` resource.

# AWS Microservice Architecture: Products Management

This section describes an AWS-based microservice architecture that provides product data through a set of API endpoints. The architecture utilizes **Amazon API Gateway**, **AWS Lambda**, and **Amazon DynamoDB** to efficiently handle requests for retrieving product information. This architecture provides a scalable, efficient solution for serving product data via a RESTful API. By utilizing AWS services such as Amazon API Gateway, AWS Lambda, and Amazon DynamoDB, the microservice ensures fast and reliable data retrieval while minimizing infrastructure management overhead.

## Architecture Overview

The microservice consists of three main AWS services:

<img src="images/Slide1.jpg" alt="My image" style="width: 100%; max-width: 1500px; height: auto;"/>

### 1. Amazon API Gateway

The **Amazon API Gateway** serves as the entry point for incoming HTTP requests. It exposes two primary endpoints:

- **GET /products**: Fetches a list of all products available in the database.
- **GET /products/{id}**: Retrieves the details of a specific product by its unique identifier (`id`).

Amazon API Gateway routes these HTTP requests to the appropriate AWS Lambda functions for processing.

### 2. AWS Lambda

Two AWS Lambda functions handle the core business logic for retrieving product data:

- **get_products**: This AWS Lambda function is invoked by the `GET /products` endpoint. It queries the Amazon DynamoDB **products** table to fetch all available products and returns them in the response.
  
- **get_product**: This AWS Lambda function is triggered by the `GET /products/{id}` endpoint. It retrieves a specific product’s details by querying the Amazon DynamoDB **products** table using the provided `id`.

Both AWS Lambda functions are responsible for processing the requests and interacting with Amazon DynamoDB.

### 3. Amazon DynamoDB

**Amazon DynamoDB** is used as the data store for the product information. The **products** table contains the following:

- **Primary Key**: Likely the product `id`, which uniquely identifies each product in the table.
- **Attributes**: Additional fields such as product name, description, price, and any other relevant product details.

The AWS Lambda functions query Amazon DynamoDB to retrieve either a list of products or a specific product by `id`.

## Flow of Requests

1. A client sends an HTTP request to the Amazon API Gateway, either to `GET /products` or `GET /products/{id}`.
2. Amazon API Gateway routes the request to the corresponding AWS Lambda function (`get_products` or `get_product`).
3. The AWS Lambda function queries Amazon DynamoDB to fetch the requested data.
4. The AWS Lambda function returns the data (a list of products or a single product) to the Amazon API Gateway.
5. Amazon API Gateway sends the response back to the client.

# AWS Microservice Architecture: Orders Management

This section describes an AWS-based microservice architecture for managing orders and inventory. The architecture utilizes **Amazon API Gateway**, **AWS Lambda**, **Amazon DynamoDB**, and **AWS Step Functions** to efficiently handle orders through API endpoints and automate order processing. The system allows for easy retrieval of orders, as well as automated processing and inventory updates when new orders are created.

## Architecture Overview

The microservice consists of the following four AWS services:

<img src="images/Slide2.jpg" alt="My image" style="width: 100%; max-width: 1500px; height: auto;"/>

### 1. Amazon API Gateway

The **Amazon API Gateway** exposes the `orders` endpoint and supports the following HTTP methods:

- **GET /orders**: Retrieves a list of all orders.
- **GET /orders/{id}**: Retrieves the details of a specific order using the order ID.
- **POST /orders**: Creates a new order.
- **GET /orders/status/{executionArn}**: Retrieves the execution status of the state machine.

Amazon API Gateway routes the requests to the appropriate AWS Lambda functions for processing.

### 2. AWS Lambda

Three AWS Lambda functions are responsible for the core business logic:

- **get_orders**: This AWS Lambda function is invoked by the `GET /orders` endpoint. It queries the **orders** table in Amazon  DynamoDB to fetch a list of all orders.
  
- **get_order**: This AWS Lambda function is invoked by the `GET /orders/{id}` endpoint. It queries the **orders** table to retrieve a specific order by its `id`.

- **create_order**: This AWS Lambda function is triggered by the `POST /orders` endpoint. It processes the creation of a new order and triggers an AWS Step Functions state machine named "New Order" for further processing. It also returns the ARN of the execution of the state machine.

- **check_order_submission**: This AWS Lambda function is invoked by the `GET /orders/status/{executionArn}` endpoint. It retrieves the status of the execution of the state machine using the ARN provided by **create_order**.

### 3. Amazon DynamoDB

The **Amazon DynamoDB** service contains two tables used in this architecture:

- **orders**: This table stores the order information. The table includes attributes such as order ID, customer details, product details, and order status.
  
- **products**: This table contains information about available products. It is used to track inventory levels, including quantities of products.

### 4. AWS Step Functions

The **AWS Step Functions** service orchestrates the processing of new orders. The state machine named **"New Order"** contains two key steps:

- **new_order**: This AWS Lambda function is executed first within the state machine. It updates the **orders** table in Amazon  DynamoDB with the new order details (such as customer information and ordered products).
  
- **update_inventory**: This AWS Lambda function is executed only if the **new_order** function is successful. It updates the **products** table in Amazon DynamoDB to reflect changes in inventory (such as reducing the stock count for ordered products).

The **"New Order"** state machine is triggered by the **create_order** AWS Lambda function when a new order is placed.

## Flow of Requests

1. A client sends an HTTP request to the Amazon API Gateway, either to `GET /orders`, `GET /orders/{id}`, `POST /orders` or `GET /orders/status/{executionArn}`.
2. **For `GET /orders` and `GET /orders/{id}`**: Amazon API Gateway routes the request to either the `get_orders` or `get_order` AWS Lambda function to retrieve the order information from the **orders** table.
3. **For `POST /orders`**: Amazon API Gateway routes the request to the `create_order` AWS Lambda function, which initiates the **"New Order"** AWS Step Functions state machine.
4. The **"New Order"** state machine starts by executing the **new_order** AWS Lambda function. This updates the **orders** table with the new order details.
5. If the **new_order** function is successful, the state machine proceeds to the **update_inventory** AWS Lambda function, which updates the **products** table to adjust inventory levels based on the products included in the order.
6. **For `GET /orders/status/{executionArn}`**: Amazon API Gateway routes the request to the `check_order_submission` AWS Lambda function to retrieve the status of execution of the state machine whose ARN is `{executionArn}`.

# Microservice Architecture: Report Generation Workflow

This section describes the architecture of a serverless microservice that generates and distributes reports using AWS services. The system uses various AWS components to retrieve data, generate reports, and send notifications with links to the generated reports. This architecture leverages:
1. **Amazon API Gateway**: Exposes the `POST /create_report` endpoint to trigger the report generation process.
2. **AWS Lambda**: Handles the logic for generating reports and orchestrating the flow.
3. **Amazon DynamoDB**: Stores `orders` and `products` data.
4. **Amazon S3**: Stores the generated HTML reports.
5. **AWS Step Functions**: Orchestrates the report generation process and coordinates parallel tasks.
6. **Amazon SNS**: Sends email notifications with pre-signed URLs for the generated reports.

## Architecture Overview

The microservice consists of the following six AWS services:

<img src="images/Slide3.jpg" alt="My image" style="width: 100%; max-width: 1500px; height: auto;"/>

## Workflow Description

### 1. **Amazon API Gateway**
   The process begins with the **Amazon API Gateway**. It exposes the endpoint `POST /create_report`, which clients use to trigger the report generation process. When a request is received, it invokes the `create_report` AWS Lambda function.

### 2. **AWS Lambda Function: `create_report`**
   The **`create_report`** AWS Lambda function is triggered by the **Amazon API Gateway**. This function initiates the AWS Step Functions state machine (`generate_report`) to begin the report generation process.

### 3. **AWS Lambda Function: `check_report_submission`**
   The **`check_report_submission`** AWS Lambda function is triggered by the **Amazon API Gateway**. This function retrieves the execution status of state machine (`generate_report`) from its ARN: `{executionArn}`.   

### 4. **Amazon DynamoDB**
   The service uses **Amazon DynamoDB** as a NoSQL database, with two key tables:
   - **`orders` table**: Stores order-related data.
   - **`products` table**: Stores product-related data.

   These tables are accessed by AWS Lambda functions in the state machine to prepare the necessary data for report generation.

### 5. **Amazon S3: `reports` Bucket**
   The generated reports are stored in **Amazon S3** within the `reports` bucket. The reports are saved in HTML format, and pre-signed URLs are generated for access to these reports.

### 6. **AWS Step Functions: `generate_report`**
   The core of the report generation process is the **AWS Step Functions** state machine named `generate_report`. This state machine coordinates multiple AWS Lambda functions that process the report data and generate the HTML reports.

   The state machine includes **parallel execution**:
   - **Orders Branch**:
     - **`prepare_orders_report_data`**: Retrieves and prepares data from the `orders` table in Amazon DynamoDB.
     - **`prepare_orders_report_html`**: Converts the prepared order data into an HTML report.
   - **Products Branch**:
     - **`prepare_products_report_data`**: Retrieves and prepares data from the `products` table in Amazon DynamoDB.
     - **`prepare_products_report_html`**: Converts the prepared product data into an HTML report.

   Both branches run concurrently, optimizing the report generation process.

### 7. **AWS Lambda Function: `generate_presigned_url`**
   After both branches complete successfully, the **`generate_presigned_url`** AWS Lambda function is executed. This function generates short-lived pre-signed URLs for the generated HTML reports stored in Amazon S3.

### 8. **Amazon SNS Notification: `html_report_notifications`**
   The final step in the state machine is the **Amazon SNS** notification. Once the pre-signed URLs are generated, an SNS email notification is sent to subscribers of the **`html_report_notifications`** topic. The email sent contains the pre-signed URLs for both the orders and products reports, allowing users to download the reports.

## Workflow Summary
1. The client sends a `POST /create_report` request to **Amazon API Gateway**.
2. **Amazon API Gateway** triggers the `create_report` AWS Lambda function.
3. **AWS Step Functions** starts the `generate_report` state machine, executing the following tasks in parallel:
   - **Orders Data Preparation** (`prepare_orders_report_data`) and **Orders HTML Generation** (`prepare_orders_report_html`).
   - **Products Data Preparation** (`prepare_products_report_data`) and **Products HTML Generation** (`prepare_products_report_html`).
4. Once the parallel tasks are completed, **`generate_presigned_url`** generates short-lived pre-signed URLs for the reports stored in Amazon S3.
5. **Amazon SNS** sends an email containing the pre-signed URLs to the subscribers of the **`html_report_notifications`** topic.
6. **For `GET /create_report/status/{executionArn}`**: Amazon API Gateway routes the request to the `check_report_submission` AWS Lambda function to retrieve the status of execution of the state machine whose ARN is `{executionArn}`.


# AWS Microservice Architecture: User Authentication with Amazon Cognito and PKCE

This AWS architecture diagram describes a microservice that facilitates user login using **Amazon Cognito** and the **Authorization Code Grant Flow with PKCE** (Proof Key for Code Exchange), commonly used for secure, user authentication in web applications. Below is the breakdown of the architecture and the steps involved in generating an access token for the user, enabling them to access protected resources in the system. The described architecture provides a secure, scalable way for users to authenticate via a webpage, leveraging AWS services such as Amazon API Gateway, AWS Lambda, and Amazon Cognito. The flow is built on the **Authorization Code Grant Flow with PKCE**, ensuring security throughout the authentication process. The user is authenticated, tokens are securely exchanged, and once logged in, they can access other microservices protected by Amazon Cognito and Amazon API Gateway.

This setup offers robust user authentication capabilities, scalability, and ease of integration with other services in the AWS ecosystem, ensuring secure communication between the frontend and backend, while adhering to best practices for OAuth2 and PKCE security protocols.

<img src="images/Slide4.jpg" alt="My image" style="width: 100%; max-width: 1500px; height: auto;"/>

## Components:
1. **Amazon API Gateway**:
   - Exposes two key endpoints for communication between the frontend (webpage) and backend services.
     - `POST /exchange-token`: Receives an authorization code and code verifier from the webpage to exchange for an access token.
     - `POST /oauth2/token`: Used internally to communicate with Amazon Cognito to exchange the authorization code for tokens.

2. **AWS Lambda**:
   - **exchange-token AWS Lambda Function**: Handles the request from the webpage, communicates with Amazon Cognito to exchange the authorization code for the access token, ID token, and refresh token.

3. **Amazon Cognito**:
   - **Cognito User Pool**: Handles authentication and authorization using the Authorization Code Grant Flow with PKCE.
   - Generates the **access token**, **ID token**, and **refresh token**, which are returned to the client (webpage).

---

## Step-by-Step Process:

1. **Step 1: User Initiates Login**  
   - The user clicks on the "login" button on the webpage. This action triggers an **authorization challenge** request to **Amazon Cognito**, which includes necessary parameters (such as client ID, redirect URI, and the PKCE code challenge).

2. **Step 2: Amazon Cognito Responds with Authorization Code**  
   - Amazon Cognito processes the authorization challenge and, if successful, returns an **authorization code** to the webpage, which will be used in the next steps of the flow.

3. **Step 3: Webpage Sends Authorization Code to Amazon API Gateway**  
   - The webpage sends the **authorization code** and a **code verifier** (part of the PKCE protocol) in a **POST request** to the `POST /exchange-token` endpoint of the **Amazon API Gateway**. This step is critical to maintain the integrity and security of the authentication process by ensuring the authorization code is exchanged securely.

4. **Step 4: AWS Lambda Function Prepares Request to Amazon Cognito**  
   - The Amazon API Gateway forwards the request to the **exchange-token AWS Lambda function**. This AWS Lambda function prepares a **POST request** to the `POST /oauth2/token` endpoint of **Amazon Cognito**. The request includes the **authorization code**, the **code verifier**, and other necessary authentication information.

5. **Step 5: AWS Lambda Function Sends Request to Amazon API Gateway**  
   - The AWS Lambda function sends the prepared request to the **Amazon API Gateway**, which acts as an intermediary between the AWS Lambda function and Amazon Cognito. The request is forwarded via the `POST /oauth2/token` endpoint.

6. **Step 6: Amazon API Gateway Forwards Request to Amazon Cognito**  
   - The Amazon API Gateway forwards the request to **Amazon Cognito**. Amazon Cognito validates the authorization code, the code verifier, and other details. If the validation is successful, Amazon Cognito proceeds to the next step.

7. **Step 7: Amazon Cognito Responds with Tokens**  
   - Amazon Cognito returns the **access token**, **ID token**, and **refresh token** in the response. These tokens are sent back to the **exchange-token AWS Lambda function**, which then returns them to the webpage via the `POST /exchange-token` endpoint.

8. **Step 8: User Successfully Logs In**  
   - Once the tokens are returned to the webpage, the user is successfully logged in and is granted access to protected resources. The access token allows the user to make authenticated requests to other microservices within the system, such as:
     - **create_report** (via `POST /create_report`)
     - **orders** (via `GET /orders`)

---

## Security Considerations (PKCE):
The **Authorization Code Grant with PKCE** is used to enhance the security of the authorization process. PKCE prevents interception of the authorization code by malicious actors, as it requires the use of a **code verifier** (a cryptographically random string) and a **code challenge** (a transformation of the code verifier) during the authentication flow. This ensures that only the legitimate client can exchange the authorization code for an access token.

---

### Licenses

In React code, I used pkce-challenge library. The copyright notice and permission notice of using pkce-challenge library is indicated below:

MIT License

Copyright (c) 2019 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

