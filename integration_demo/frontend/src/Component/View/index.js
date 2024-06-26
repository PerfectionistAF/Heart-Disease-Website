import React, { Component, useEffect, useState } from 'react'
import './style.css';
import { Link, useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import axios from 'axios';



const View = () => {


    const location = useLocation();
    const { patientId } = location.state || { patientId: null };
    const navigate = useNavigate();
    const [patient, setPatient] = useState({});
    const [patientFiles, setPatientFiles] = useState([]);
    const [error, setError] = useState('');


    useEffect(() => {
        const fetchPatients = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_API_URL}patients/${patientId}`);
                setPatient(response.data);
            } catch (error) {
                setError('There was an error fetching the patient');
                console.error('Error fetching patient:', error);
            }
        };

        const fetchPatientFiles = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_API_URL}doctor-patient-files/?name=&patient=${patientId}`);
                setPatientFiles(response.data);
            } catch (error) {
                setError('There was an error fetching the patient files');
                console.error('Error fetching patient files:', error);
            }
        };

        fetchPatients();
        fetchPatientFiles();
    }, []);

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-CA');
    };



    return (
        <div className='View_section'>
            <div className="patient-data-container">
                <h2>Patient Data</h2>
                <div className='Roww'>
                    <strong>Name:</strong> {patient.name}
                </div>

                <div className='Roww'>
                    <strong>Phone Number:</strong> {patient.phone_number}
                </div>

                {/* <div className='Roww'>
                    <strong>Email Address:</strong> {Alimohamed@gmail.com}
                </div> */}

                <div className='Roww'>
                    <strong>Address:</strong> {patient.address}
                </div>

                <div className='Roww'>
                    <strong>Birthdate:</strong> {formatDate(patient.birthdate)}
                </div>

                {patientFiles.map((file, index) => (
                    <div className='Roww' key={file.id}>
                        <p>

                            <strong>Test {index + 1} Date:</strong> {formatDate(file.created_at)}
                            <br />
                            <strong> Result:</strong> {file.final_diagnosis}
                            <br />
                            <Link to={`/TestView/${file.id}`}>
                                <button className={`vview_button2`}> View </button>
                            </Link>
                        </p>
                    </div>
                ))}

            </div>
        </div>
    )
}

export default View;