import React from "react";
import { useLocation  } from "react-router-dom";
import { useEffect, useState, useRef } from 'react'
import pkceChallenge from 'pkce-challenge';

const COGNITO_AUTH_URL = import.meta.env.VITE_COGNITO_AUTH_URL;
const CLIENT_ID = import.meta.env.VITE_CLIENT_ID;
const REDIRECT_URI = import.meta.env.VITE_REDIRECT_URI;

const SignIn = () => {
    const location = useLocation();
    const { isUserSignedIn } = location.state || {};  // Default to empty object if no state is passed    

    const [codeVerifier, setCodeVerifier] = useState('');
    const [codeChallenge, setCodeChallenge] = useState('');

    const hasRun = useRef(false);

    useEffect(() => {
        console.log('hasRun.current (initial):', hasRun.current);
        const generatePKCE = async () => {
        if (!hasRun.current)
        {
          try {
            const pkce = pkceChallenge(); // pkceChallenge is now returning a Promise
            const { code_verifier, code_challenge } = await pkce; // Wait for Promise to resolve
                        
            setCodeVerifier(code_verifier);            
            setCodeChallenge(code_challenge);

            // When Cognito returns with a code challenge, App.jsx is re-rendered, and any variable
            // that is passed to CallbackSignIn is reset. For this reason, I store code_verifier in localStorage 
            // instead of passing it to CallbackSignIn. Inside CallbackSignIn, I retrieve it from the localStorage.
            localStorage.setItem('codeVerifier', code_verifier);

            hasRun.current = true;

          } catch (error) {
            console.error("Error generating PKCE: ", error);
          }
        }
        
      };

      generatePKCE();
    }, []);

    useEffect(() => {
        try {
            if (!isUserSignedIn && codeChallenge)
            {
                signIn()
            }            
        } catch (error) {
          console.error("Error signing in: ", error);
        }
    }, [codeChallenge, isUserSignedIn]);
    
    const signIn = () => {
      setTimeout(() => {
        window.location.href = `${COGNITO_AUTH_URL}/login?client_id=${CLIENT_ID}&response_type=code&scope=email+openid&redirect_uri=${REDIRECT_URI}&code_challenge=${codeChallenge}&code_challenge_method=S256`;
      }, 1000);
    };

    return (
      <div>
        <p>Redirecting to sign-in...</p>
      </div>
    );
  
};

export default SignIn;
