import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_GATEWAY_BASE_URL = import.meta.env.VITE_API_GATEWAY_URL;
const CLIENT_ID = import.meta.env.VITE_CLIENT_ID;
const REDIRECT_URI = import.meta.env.VITE_REDIRECT_URI;

const CallbackSignIn = ({onCodeReceived, handleSignIn }) => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {    
    const urlParams = new URLSearchParams(window.location.search);
    const authorizationCode = urlParams.get('code');
    const { isUserSignedIn } = location.state || {};  // Default to empty object if no state is passed 

    const codeVerifier = localStorage.getItem('codeVerifier');

    if (authorizationCode && codeVerifier && !isUserSignedIn) {
        handleAuthorizationCode(authorizationCode, codeVerifier);
        onCodeReceived(authorizationCode);
    } else {
      console.error('Authorization code not found');
    }
  }, [navigate, location, onCodeReceived]);
  
  const handleAuthorizationCode = (authorizationCode, codeVerifier) => {
    // Prepare the payload for the token exchange
    const tokenRequestData = {
      grant_type: 'authorization_code',
      client_id: CLIENT_ID,
      code: authorizationCode, // The authorization code from the URL
      redirect_uri: REDIRECT_URI, // Same as the one used in the initial request
      code_verifier: codeVerifier // This is the code_verifier generated earlier
    };

    // Send the request to API Gateway which will forward to Lambda, which will send
    // Cognito's token endpoint to exchange the code for tokens
    axios.post(`${API_GATEWAY_BASE_URL}/exchange-token`, tokenRequestData)
    .then((response) => {
      const { access_token, id_token, refresh_token } = response.data;

      localStorage.setItem('accessToken', access_token);
      localStorage.setItem('idToken', id_token);
      localStorage.setItem('refreshToken', refresh_token);

      handleSignIn();
    })
    .catch((error) => {
      console.error('Error exchanging code for tokens:', error);
    });
  };
      
      
};

export default CallbackSignIn;