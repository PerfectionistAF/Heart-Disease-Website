import React, { Component, useState, useEffect } from 'react'
import './style.css';
import axios from 'axios';
import { Link, useParams, useNavigate } from 'react-router-dom';
import GradientSlider from '../GradientSlider';
import { getIntegDiagnosisKey } from '../../constants';


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

                    {file.rf_diagnosis && (
                        <>

                            <label className='Section_name'> Tabular Data Section </label>



                            <label className='Patientlabel' htmlFor="age">Age</label>
                            <label className='viewPatientinput'  > {file.age}</label>


                            <label className='Patientlabel' htmlFor="Sex">Sex</label>
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

                            <label className='Diagnosislabel' htmlFor="diagnosis">RiskFactors_GB Diagnosis</label>
                            <label className='viewDiagnosis'>{file.rf_diagnosis}</label>

                        </>
                    )}






                    {file.ecg_diagnosis && (
                        <>
                            <label className='Section_name'> ESG Section</label>
                            <label className='Patientlabel' htmlFor="ecg-image">Uploaded ECG Image:</label>
                            <label className='viewPatientimg'>

                                <label htmlFor="image_ii">
                                    ECG channel_II
                                </label>
                                <img name="image_ii" id="image_ii" src={file.image_ii} alt="ECG image channel_ii" width='400'></img>

                                <hr />
                                <label htmlFor="image_v6">
                                    ECG channel_V6
                                </label>
                                <img name="image_v6" id="image_v6" src={file.image_v6} alt="ECG image channel_v6" width='400'></img>


                                <hr />
                                <label htmlFor="image_vz">
                                    ECG channel_VZ
                                </label>
                                <img name="image_vz" id="image_vz" src={file.image_vz} alt="ECG image channel_vz" width='400'></img>

                            </label>
                            <label className='Diagnosislabel' htmlFor="diagnosis">ECG_ResNet50 Diagnosis</label>
                            <label className='viewDiagnosis'>{file.ecg_diagnosis}</label>

                        </>
                    )}

                    {file.echo_diagnosis && (
                        <>
                            <label className='Section_name'> Echocardiography Section</label>
                            <label className='Patientlabel' htmlFor="echo-video">Uploaded Echocardiography Video:  </label>
                            <label className='viewPatientvideo'>
                                <video controls width="400">
                                    <source src={file.video} type="video/avi" />
                                    Your browser does not support the video tag.
                                </video>
                            </label>
                            <label className='Diagnosislabel' htmlFor="diagnosis">Echo_LadderNet Diagnosis</label>
                            <label className='viewDiagnosis'>{file.echo_diagnosis}</label>
                        </>
                    )}


                    {/* <hr /> */}
                    <label className='Section_name'> Final/ Integrated Diagnosis</label>
                    <label className='Patientlabel'>Diagnosis Severity Scale</label>
                    <GradientSlider value={file.final_diagnosis} />
                    <label className='viewDiagnosis'>{file.final_diagnosis}</label>



                </form>
            </div>
        </div>
    )
}

export default TestView;