import React, { Component, useState, useEffect } from 'react'
import './style.css';
import axios from 'axios';
import { Link, useParams, useNavigate } from 'react-router-dom';




const TestView = () => {


    const { fileId } = useParams();
    const [file, setFile] = useState('');


    useEffect(() => {
        const fetchPatientFile = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_API_URL}doctor-patient-files/${fileId}`);
                setFile(response.data);
            } catch (error) {
                setError('There was an error fetching the patient files');
                console.error('Error fetching patient files:', error);
            }
        };

        fetchPatientFile();
    }, []);

    return (
        <div className='Add_patient_section'>
            <div className='Container'>
                <h2>
                </h2>
                <form className='Patientform'>
                    <label className='Section_name'> Tabular Data Section </label>



                    <label className='Patientlabel' for="age">Age</label>
                    <label className='viewPatientinput'  > {file.age}</label>


                    <label className='Patientlabel' for="Sex">Sex</label>
                    <label className='viewPatientinput'  > {file.sex === 1 ? ('Male') : ('Female')}</label>

                    <label className='Patientlabel' htmlFor="cp">Chest Pain Type</label>
                    <label className='viewPatientinput'>
                        {file.cp === '1' ? 'Typical Angina' : file.cp === '2' ? 'Atypical Angina' : file.cp === '3' ? 'Non-Anginal Pain' : 'Asymptomatic'}
                    </label>


                    <label className='Patientlabel' htmlFor="trestbps">Resting Blood Pressure</label>
                    <label className='viewPatientinput'>{file.trestbps}</label>

                    <label className='Patientlabel' htmlFor="chol">Cholesterol</label>
                    <label className='viewPatientinput'>{file.chol}</label>

                    <label className='Patientlabel' htmlFor="fbs">Fasting Blood Sugar &gt; 120 mg/dl</label>
                    <label className='viewPatientinput'>{file.fbs === '1' ? 'True' : 'False'}</label>

                    <label className='Patientlabel' htmlFor="restecg">Resting Electrocardiographic Results</label>
                    <label className='viewPatientinput'>{file.restecg === '0' ? 'Normal' : file.restecg === '1' ? 'Abnormal - ST-T wave' : 'Abnormal - Left Ventricular Hypertrophy'}</label>

                    <label className='Patientlabel' htmlFor="thalach">Maximum Heart Rate Achieved</label>
                    <label className='viewPatientinput'>{file.thalach}</label>


                    <label className='Patientlabel' htmlFor="exang">Exercise Induced Angina</label>
                    <label className='viewPatientinput'>{file.exang === '1' ? 'Yes' : 'No'}</label>

                    <label className='Patientlabel' htmlFor="oldpeak">ST Depression</label>
                    <label className='viewPatientinput'>{file.oldpeak}</label>

                    <label className='Patientlabel' htmlFor="slope">Slope</label>
                    <label className='viewPatientinput'>{file.slope === '1' ? 'Upsloping' : file.slope === '2' ? 'Flat' : 'Downsloping'}</label>

                    <label className='Patientlabel' htmlFor="ca">Number of Major Vessels (0.0-3.0) Colored by Fluoroscopy</label>
                    <label className='viewPatientinput'>{file.ca}</label>

                    <label className='Patientlabel' htmlFor="thal">Thallium Stress Test Result</label>
                    <label className='viewPatientinput'>{file.thal === '3' ? 'Normal' : file.thal === '6' ? 'Fixed Defect' : 'Reversible Defect'}</label>

                    <label className='Diagnosislabel' htmlFor="diagnosis">Diagnosis</label>
                    <label className='viewDiagnosis'>{file.diagnosis}</label>







                    <label className='Section_name'> ESG Section</label>
                    <label className='Patientlabel' for="ecg-image">Uploaded ECG Image:</label>
                    <label className='viewPatientimg'>
                        <img src={file.image} alt="Image" width='400'></img>

                    </label>


                    <label className='Section_name'> Echocardiography Section</label>
                    <label className='Patientlabel' for="echo-video">Uploaded Echocardiography Video:  </label>
                    <label className='viewPatientvideo'>
                        <video src={file.video} controls width="400">
                            <source type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>
                    </label>





                </form>
            </div>
        </div>
    )
}

export default TestView;