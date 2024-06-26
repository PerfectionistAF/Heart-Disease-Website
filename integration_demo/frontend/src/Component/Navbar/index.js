import React, { Component } from 'react'
import { Iconn, Navbarsection, Container, Logo, LogoText, Ulist, ListItem, Anchor, LINK } from './style.js'
import { Link, useNavigate } from 'react-router-dom';
import './stylee.css';
import authService from '../../authService.js';



import styled from 'styled-components';


const Navbar = ({ user }) => {

    const navigate = useNavigate();
    const handleLogout = () => {
        authService.logout();
        navigate('/Login');
    };

    return (
        <div className='Navbarsection'>

            <div className='Containerr'>
                <i className=" icon fa fa-heartbeat fa-2x Icon" ></i>
                <div className='Logo'>
                    <h2 className='LogoText'>    Heart Detect  </h2>
                </div>

                <ul className='Ulist'>
                    <li className='ListItem'> <Link className='LINK' to='/'> Home </Link> </li>
                    <li className='ListItem'> <a className='Anchor' href='#'> About </a> </li>
                    <li className='ListItem'> <Link className='LINK' to='/contact'> Contact </Link> </li>
                    < li className='ListItem'> <a className='Anchor' onClick={handleLogout}> Logout </a> </li>

                    {/* {user ? (
                    ) : (<>
                        <li className='ListItem'> <Link className='LINK' to='/Signup'> Register </Link>
                        </li><li className='ListItem'> <Link className='Anchor' to='/Login'> Login </Link> </li>
                    </>)} */}


                </ul>


            </div>

        </div >
    )
}

export default Navbar;