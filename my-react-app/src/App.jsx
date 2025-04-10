import { useEffect, useState, useRef } from 'react'
import './App.css'
import {Routes, Route, useLocation, Link} from "react-router-dom";
import EntityName from './components/HeaderEntityName'
import EventName from './components/HeaderEventName'
import Products from './components/Products'
import Header from './components/Header'
import Footer from './components/Footer'
import Orders from './components/Orders'
import OrderDetail from './components/OrderDetail'
import CustomerInfoForm from "./components/CustomerInfoForm";
import CallbackSignIn from './components/CallbackSignIn'
import Home from './components/Home';
import About from './components/About';
import GenerateReport from './components/GenerateReport';
import SignOut from './components/SignOut';
import SignIn from './components/SignIn';

function App() {

  const location = useLocation();
  const [authorizationCode, setAuthorizationCode] = useState(null);
  const [isUserSignedIn, setIsUserSignedIn] = useState(false);
  const [isTestingUserSignedIn, setIsTestingUserSignedIn] = useState(true);

  const handleSignOut = () => {
    setIsUserSignedIn(false);
  };

  const handleSignIn = () => {
    setIsUserSignedIn(true);
  }; 
 
  if (
    localStorage.getItem("accessToken") == null ||
    localStorage.getItem("accessToken") == ""
  ) {
    if (window.location.hash != null && window.location.hash != "") {
      const str = window.location.hash;
      const regex = /#id_token=([^&]+)/;
      const match = str.match(regex);

      if (match) {
        const idTokenValue = match[1];
        localStorage.setItem("accessToken", idTokenValue);
      } else {
        console.log("No match found");
      }
    }
  }

  return (
    <>
    <div>
      <EntityName entityname="company_logo.jpeg" />
    </div>        
    <div>
        <Header isUserSignedIn={isUserSignedIn} authorizationCode={authorizationCode} isTestingUserSignedIn={isTestingUserSignedIn}/>
        {isUserSignedIn ? 
        (
          // Render content for signed-in users
          <div>
            <div>Signed in as employee</div>                                   
          </div>
        ) : 
        (
          isTestingUserSignedIn ?
          (
            // Render content for signed-in users
            <div>
              <div>You are in Test mode</div>                                   
            </div>
          ) : null
        )
      }
      </div>
    <div>
      {/* Render Event banner only for specific routes */}
      {location.pathname !== '/customerinfoform' &&
      location.pathname !== '/about' &&
      location.pathname !== '/generatereport' && <EventName eventname="event_banner.jpeg" />}
    </div>
    <Routes>
      <Route path="/home" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/products" element={<Products />} />
      <Route path="/orders" element={<Orders />} />
      <Route path="/orders/:id" element={<OrderDetail />} />
      <Route path="/customerinfoform" element={<CustomerInfoForm />} />
      <Route path="/callback" element={<CallbackSignIn onCodeReceived={setAuthorizationCode} handleSignIn={handleSignIn}/>} />
      <Route path="/generatereport" element={<GenerateReport />} />
      <Route path="/signout" element={<SignOut handleSignOut={handleSignOut} />} />
      <Route path="/signin" element={<SignIn />} />
    </Routes>
    <Footer />         
    </>
  )
}

export default App
