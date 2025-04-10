import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { BrowserRouter } from "react-router-dom";

createRoot(document.getElementById('root')).render(
  //I noticed that generatePKCE is called twice no matter what I do. According to Meta AI:
  //"The code is executed twice likely due to a common issue in React applications: Strict Mode
  // React Strict Mode is a development mode that helps you identify potential issues in your application.
  // It's enabled by default in Create React App".
  //So, I disabled StrictMode.

  //<StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  //</StrictMode>,
)
