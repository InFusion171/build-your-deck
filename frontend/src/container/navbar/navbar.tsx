import React from 'react'

import { Link } from 'react-router-dom';

import "./navbar.css";

const Navbar = () => {
  
  return (
    <>
      <div className='navbar-container'>
        <div className='navbar-logo'>
            <Link to="/">Logo</Link>
        </div>
        <div className='navbar-wardecks'>
            <Link to="/wardecks">Wardecks</Link>
        </div>
      </div>
      
      <hr />
    </>
  )
}

export default Navbar