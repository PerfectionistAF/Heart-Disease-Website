import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { Link } from 'react-router-dom'
import './App.css';
import About from './Component/About'
import Contact from './Component/Contact'

import Home from './Component/Home'
import Navbar from './Component/Navbar'
import Navbar_main from './Component/Navbar_main'

import Index from './Component/Indexx'
import New_Patient from './Component/New_Patient'
import Add_Patient from './Component/Add_Patient'
import Result from './Component/Result'
import Login from './Component/Login'
import Signup from './Component/Signup'
import Patient_File_Parent from './Component/Patient_File_Parent';
import View from './Component/View'
import TestView from './Component/TestView'
import ProtectedRoute from './ProtectedRoute.js';
import React, { Component, useState, useEffect } from 'react';



const App = () => {
  // render() {


  const user = localStorage.getItem('access') !== null;



  return (
    <Router>

      {user ?
        (<Navbar />)
        : (<Navbar_main />)}

      <Routes>

        <Route path="/Contact" element={<Contact />} />
        <Route path="/Login" element={<Login />} />
        <Route path="/Signup" element={<Signup />} />



        {/* Protected routes for authenticated users only */}
        <Route path="/" element={<ProtectedRoute element={<Index />} />} />




        <Route path="/New_Patient" element={<ProtectedRoute element={<Patient_File_Parent showNewPatient={true} />} />} /> {// add a submission for a new patient 
        }
        <Route path="/Add_Patient/:patientId" element={<ProtectedRoute element={<Patient_File_Parent showNewPatient={false} />} />} />{// add submission for pre-existing patient 
        }




        <Route path="/TestView/:fileId" element={<ProtectedRoute element={<TestView />} />} /> {// view a single test 
        }
        <Route path="/Result" element={<ProtectedRoute element={<Result />} />} /> {// model prediction output after submission 
        }
        <Route path="/View" element={<ProtectedRoute element={<View />} />} /> {// view the patient and all his results 
        }



        {/* <Redirect from="/" to="/home" /> */}
      </Routes>





    </Router>
  )

}

export default App;
