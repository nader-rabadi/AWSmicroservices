import React from "react";
import { useEffect, useState } from 'react'
import axios from 'axios'

const API_GATEWAY_BASE_URL = import.meta.env.VITE_API_GATEWAY_URL;

const GenerateReport = () => {

    const [isDisplayWaitMessage, setIsDisplayWaitMessage] = useState(false);
    const [isDisplayReportStatus, setIsDisplayReportStatus] = useState(false);
    const [submissionError, setSubmissionError] = useState("");
    const [testexecutionArn, setTestExecutionArn] = useState("");
    const [ordersMessage, setOrdersMessage] = useState("");
    const [productsMessage, setProductsMessage] = useState("");

    useEffect(() => {
        try {
            handleGenerateReport()
        } catch (error) {
          console.error("Error generating report: ", error);
        }
    }, []);

    const createReport = async () => {
        try {
            const response = await axios.post(`${API_GATEWAY_BASE_URL}/create-report`, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.status === 202) {                        
                // Poll for status
                const { executionArn } = response.data;                
                let orderStatus = 'RUNNING';
            
                while (orderStatus === 'RUNNING') {
                    const statusResponse = await axios.get(`${API_GATEWAY_BASE_URL}/create-report/status/${executionArn}`, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                    });
                
                    const statusData = statusResponse.data;
                    orderStatus = statusData.status;

                    if (orderStatus === 'SUCCEEDED') {
                        setTestExecutionArn(executionArn);         
                        return {'orderStatus':orderStatus, 'executionArn':executionArn};
                    } else if (orderStatus === 'FAILED' || orderStatus === 'TIMED_OUT' || orderStatus === 'ABORTED') {
                        throw new Error(`Report processing failed: ${statusData.output}`);
                    }
                
                    // Wait before the next poll
                    await new Promise(resolve => setTimeout(resolve, 2000));
                }
            } else {          
            throw new Error(`Report processing failed: ${response.status}`);
            }
        } catch (error) {
            console.log('Error:', error);
            setSubmissionError("Your order is not submitted. An error occurred at our servers. Please contact us and provide us with the error message: " + error.message);        
            throw error;
        }
    };

    const getReport = async () => {
        try {
            console.log('testexecutionArn = ', testexecutionArn)
            const response = await axios.get(`${API_GATEWAY_BASE_URL}/get-presigned-urls/${testexecutionArn}`, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            console.log('response = ', response)
            console.log('response.data.urloutputs = ', response.data.urloutputs)

            if (response.status === 200) {                        
                // Poll for status
                return response.data.urloutputs;
                           
            } else {        
            throw new Error(`Report processing failed getting report: ${response.status}`);
            }
        } catch (error) {
            console.log('Error:', error);
            setSubmissionError("Your order is not submitted. An error occurred at our servers. Please contact us and provide us with the error message: " + error.message);        
            throw error;
        }
    };    

    const handleGenerateReport = async () => {

      // Set loading state to true when form is being submitted
      setIsDisplayWaitMessage(true);
        
      try {
          const result = await createReport();      
          setIsDisplayWaitMessage(false);
          setIsDisplayReportStatus(true);
      } catch (error) {
          console.log('Error processing report:', error);
          setIsDisplayWaitMessage(false);
          setIsDisplayReportStatus(true);
      }
    };

    useEffect(() => {
        if (testexecutionArn) {
            handleGetReport();
        }
    }, [testexecutionArn]); // This effect runs when testexecutionArn changes

    const handleGetReport = async () => {
          
        try {
            const result = await getReport(testexecutionArn)
            const urldict = JSON.parse(result)
            setOrdersMessage(urldict['presigned_url_orders_str']['presigned_url_orders_str']);
            setProductsMessage(urldict['presigned_url_products_str']['presigned_url_products_str']);
        } catch (error) {
            console.log('Error processing report:', error);
        }
    };

    const displayWaitMessage = () => {
      return <div><h3>Processing Report Generation ...</h3></div>;
    }
  
    return (
        <>
      <div>
        {isDisplayWaitMessage ?
        (
            displayWaitMessage()
        ) :
        isDisplayReportStatus ?
        (
            <>
        <div>
            <h3>{submissionError ? "Error" : "Success"}</h3>
            <p>{submissionError || "Your request has been submitted successfully. Reports are sent to your registered email."}</p>
        </div>
        <div style={{ textAlign: 'left',
            wordWrap: 'break-word',
            wordBreak: 'break-word',
            maxWidth: '100%',
            whiteSpace: 'normal'
            }}>
            <p>If you are subscribed to the AWS SNS topic <strong>HtmlReportNotifications</strong>, then the notification you 
                will receive contains two URLs: one for the Orders report, and the other is for the Products report. These URLs
                are generated with an expiration time of 60 minutes (see EXPIRATION_IN_SECOND in generate_presigned_url.py).</p>
            <p>For testing purpose, I am including these URLs below.</p>
            <p><strong>Orders Report URL:</strong></p>
            <div>
                <a href={ordersMessage} target="_blank" rel="noopener noreferrer">
                    {ordersMessage}
                </a>
            </div>
            <p><strong>Products Report URL</strong></p>
            <div>
                <a href={productsMessage} target="_blank" rel="noopener noreferrer">
                    {productsMessage}
                </a>
            </div>
        </div>
        </>
        ) :
        null 
        }
      </div>
      
      </>                             
    )  

};

export default GenerateReport;
