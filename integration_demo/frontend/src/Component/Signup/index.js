import React, { useState, useEffect, Component } from 'react'
import './style.css'
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import authService from '../../authService';

const Signup = () => {

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    address: '',
    specialization: '',
    // birthdate: '',

    // confirmPassword: ''
  });

  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // console.log('User registered:', formData.email,
    //   formData.password,
    //   formData.first_name,
    //   formData.last_name,
    //   formData.phone_number,
    //   formData.address,
    //   formData.specialization,
    // );
    try {
      const response = await authService.register(
        formData
      );
      console.log('User registered:', response.data);
      navigate('/');
    } catch (error) {
      console.error('Registration error:', error.response ? error.response.data : error);
      setError('There was an error registering the user!');
    }
  };


  return (
    <div className="signup-container">
      <h2>Sign Up</h2>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="first_name">First Name:</label>
          <input type="text" id="first_name" name="first_name" value={formData.first_name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="last_name">Last Name:</label>
          <input type="text" id="last_name" name="last_name" value={formData.last_name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input type="email" id="email" name="email" value={formData.email} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="address">Address:</label>
          <input type="text" id="address" name="address" value={formData.address} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="phone_number">Phone Number:</label>
          <input type="tel" id="phone_number" name="phone_number" value={formData.phone_number} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="specialization">Specialization:</label>
          <input type="text" id="specialization" name="specialization" value={formData.specialization} onChange={handleChange} required />
        </div>
        {/* <div className="form-group">
                <label htmlFor="birthdate">Birthdate:</label>
                <input type="date" id="birthdate" name="birthdate" value={formData.birthdate} onChange={handleChange} required />
                </div> */}
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input type="password" id="password" name="password" value={formData.password} onChange={handleChange} required />
        </div>

        {/* <Link to="/"> */}
        <button type="submit">Sign Up</button>
        {/* </Link> */}
        <div className="signup-link">
          <p>Already have an account? <Link to="/Login">Login</Link></p>
        </div>

        {error && <p>{error}</p>}
      </form>
    </div>

  )
}

export default Signup;