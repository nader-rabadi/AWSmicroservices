import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import axios from "axios";

const API_GATEWAY_BASE_URL = import.meta.env.VITE_API_GATEWAY_URL;

const CustomerInfoForm = () => {

  const [personalInfo, setPersonalInfo] = useState({
    customer_name: "",
    email: "",
    phone: ""
  });

  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [submissionError, setSubmissionError] = useState("");
  const location = useLocation();  
  const [customerproduct, setCustomerProduct] = useState(null);

  useEffect(() => {
    if (location.state) {
      setCustomerProduct(location.state);
    }
  }, [location]);

  if (!customerproduct) {
    return <div><h3>Please wait...</h3></div>;
  }

  const handleChange = (e) => {
    const { name, value } = e.target;
    setPersonalInfo({
      ...personalInfo,
      [name]: value,
    });
  };

  const createOrder = async (dataToSubmit) => {
    try {
        const response = await axios.post(`${API_GATEWAY_BASE_URL}/orders`, dataToSubmit, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
                
        if (response.status === 202) {                        
            // Poll for status
            const { executionArn } = response.data;
            let orderStatus = 'RUNNING';

            while (orderStatus === 'RUNNING') {
                const statusResponse = await axios.get(`${API_GATEWAY_BASE_URL}/orders/status/${executionArn}`, {
                  headers: {
                    'Content-Type': 'application/json'
                  }
                });

                const statusData = statusResponse.data;
                orderStatus = statusData.status;
                
                if (orderStatus === 'SUCCEEDED') {                
                    return orderStatus;
                } else if (orderStatus === 'FAILED' || orderStatus === 'TIMED_OUT' || orderStatus === 'ABORTED') {
                    throw new Error(`Order processing failed: ${statusData.output}`);
                }

                // Wait before the next poll
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        } else {          
          throw new Error(`Order processing failed: ${response.status}`);
        }
    } catch (error) {
        console.log('Error:', error);
        setSubmissionError("Your order is not submitted. An error occurred at our servers. Please contact us and provide us with the error message: " + error.message);        
        throw error;
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setIsLoading(true);
    
    // Combine both objects into one
    const dataToSubmit = {
          personalInfo,
          customerproduct
        }

    try {
        const result = await createOrder(dataToSubmit);
        setIsLoading(false);
        setIsSubmitted(true);
    } catch (error) {
        console.log('Error processing order:', error);
        setIsLoading(false);
        setIsSubmitted(true);
    }
  };

  const displayWaitMessage = () => {
    return <div><h3>Please wait...</h3></div>;
  }

  return (
    <div>
      {isLoading ? (
        displayWaitMessage()
      ) : !isSubmitted ? (
              <form className="form" onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Name:</label>
                <input
                  type="text"
                  name="customer_name"
                  value={personalInfo.customer_name}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label>Email:</label>
                <input
                  type="email"
                  name="email"
                  value={personalInfo.email}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label>Phone:</label>
                <input
                  type="tel"
                  name="phone"
                  value={personalInfo.phone}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label>Credit Card Number:</label>
                <input type="text" name="creditCardNumber" value="" disabled />
              </div>
              <div className="form-group">
                <label>Expiration Date (MM/YY):</label>
                <input type="text" name="expirationDate" value="" disabled />
              </div>
              <div className="form-group">
                <label>CVC:</label>
                <input type="text" name="cvc" value="" disabled />
              </div>
              <div>
                <input type="submit" value="Submit" />
              </div>
            </form>
      ) : (
        <div>
          <h3>{submissionError ? "Error" : "Success"}</h3>
          <p>{submissionError || "Your order has been submitted successfully."}</p>
        </div>
      )}
    </div>
  );  
}

export default CustomerInfoForm;
