import { useLocation  } from "react-router-dom";
import { useEffect } from 'react'

const COGNITO_AUTH_URL = import.meta.env.VITE_COGNITO_AUTH_URL;
const CLIENT_ID = import.meta.env.VITE_CLIENT_ID;
const REDIRECT_URI = import.meta.env.VITE_REDIRECT_URI;

const SignOut = ({ handleSignOut }) => {
    const location = useLocation();
    const { isUserSignedIn, codeChallenge } = location.state || {};  // Default to empty object if no state is passed

    useEffect(() => {
        try {
            if (isUserSignedIn)
            {
                signOut()
            }            
        } catch (error) {
          console.error("Error signing out: ", error);
        }
    }, []);

    const signOut = () => {
        localStorage.removeItem("accessToken");
        localStorage.clear();

        if (handleSignOut)
        {
            handleSignOut();
        }          
  
        // Wait
        setTimeout(() => {  
          window.location.href = `${COGNITO_AUTH_URL}/logout?client_id=${CLIENT_ID}&response_type=code&scope=email+openid&logout_uri=${REDIRECT_URI}&redirect_uri=${REDIRECT_URI}&code_challenge=${codeChallenge}&code_challenge_method=S256`;
        }, 1000);
      };

    return
  
};

export default SignOut;
