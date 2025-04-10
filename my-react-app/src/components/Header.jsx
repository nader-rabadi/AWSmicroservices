import React from 'react'
import { Link } from 'react-router-dom'

const Header = ({isUserSignedIn, codeChallenge, isTestingUserSignedIn}) => {
  return (
    <div className='header'>
        <nav className='navigation'>
            <ul>
                <li><Link to="/home">Home</Link></li>
                <li><Link to="/about">About Us</Link></li>
                <li><Link to="/products">Our Cookies</Link></li>                
                {
                    isUserSignedIn ?
                    (
                        <>
                        <li><Link to="/orders">Orders</Link></li>
                        <li><Link to="/generatereport">Generate Report</Link></li>
                        <li><Link to="/signout" state={{ isUserSignedIn, codeChallenge }}>Sign Out</Link></li>
                        </>
                    ) :
                    (
                        isTestingUserSignedIn ?
                        (
                            <>
                            <li><Link to="/orders">Orders</Link></li>
                            <li><Link to="/generatereport">Generate Report</Link></li>
                            <li><Link to="/signout" state={{ isUserSignedIn, codeChallenge }}>Sign Out</Link></li>                    
                            <li><Link to="/signin" state={{ isUserSignedIn }}>Employee Sign In</Link></li>
                            </>
                        ) :
                        (
                            <li><Link to="/signin" state={{ isUserSignedIn }}>Employee Sign In</Link></li>
                        )                        
                    )
                }
            </ul>
        </nav>        
    </div>
  )
}

export default Header