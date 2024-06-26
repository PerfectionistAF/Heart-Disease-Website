import React, { useState, useEffect, Component } from 'react'
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import authService from '../../authService';
import './style.css'

const Login = () => {

    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });

    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        // console.log("User logged in: ", formData.email, formData.password);
        try {
            const response = await authService.login(formData.email, formData.password);
            console.log('User logged in:', response.user);
            if (response.access && response.refresh && response.user) {
                navigate('/');
            } else {
                setError('Failed to login, please try again.');
            }
        } catch (error) {
            setError('Invalid email or password');
            console.error('There was an error logging in the user!', error);
        }
    };

    return (
        <div className='Login_section'>
            <div className="login-container">
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="email">Email:</label>
                        <input type="email" id="email" name="email" onChange={handleChange} value={formData.email} required />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password:</label>
                        <input type="password" id="password" name="password" onChange={handleChange} value={formData.password} required />
                    </div>
                    {/* <Link to="/"> */}
                    <button type="submit">Login</button>
                    {/* </Link> */}

                    {error && <p style={{ color: 'red' }}>{error}</p>}
                </form>
                <div className="signup-link">
                    <p>Don't have an account? <Link to="/signup">Sign up</Link></p>
                </div>
            </div>
        </div>
    )
}

export default Login;