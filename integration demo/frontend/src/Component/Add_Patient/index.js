
import './style.css';
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const Add_Patient = ({ formData, onInputChange, onFileUpload }) => {


    return (
        <div >
            {/* <div className='Container'> */}
            <form className='Patientform'>

                <div>
                    <label className='Section_name'>Tabular Data Section</label>


                    <label className='Patientlabel' htmlFor="age">Age</label>
                    <input
                        className='Patientinput'
                        type="number"
                        id="age"
                        name="age"
                        placeholder='Patient Age'
                        value={formData.age}
                        onChange={onInputChange}
                        required
                    />

                    <label className='Patientlabel' htmlFor="sex">Sex</label>
                    <select
                        className='Patientinput'
                        id="sex"
                        name="sex"
                        value={formData.sex}
                        onChange={onInputChange}
                        required
                    >
                        <option value="" disabled>Select Male or Female</option>
                        <option value="1">Male</option>
                        <option value="0">Female</option>
                    </select>

                    <label className='Patientlabel' htmlFor="cp">Chest Pain Type</label>
                    <select
                        className='Patientinput'
                        id="cp"
                        name="cp"
                        value={formData.cp}
                        onChange={onInputChange}
                        required
                    >
                        <option value="" disabled>Select chest pain type</option>
                        <option value="1">Typical Angina</option>
                        <option value="2">Atypical Angina</option>
                        <option value="3">Non-Anginal Pain</option>
                        <option value="4">Asymptomatic</option>
                    </select>

                    <label className='Patientlabel' htmlFor="trestbps">Resting Blood Pressure</label>
                    <input
                        className='Patientinput'
                        type="number"
                        id="trestbps"
                        name="trestbps"
                        placeholder='The resting blood pressure in mmHg'
                        value={formData.trestbps}
                        onChange={onInputChange}
                        required
                    />

                    <label className='Patientlabel' htmlFor="chol">Cholesterol</label>
                    <input
                        className='Patientinput'
                        type="number"
                        id="chol"
                        name="chol"
                        placeholder='The serum cholesterol level in mg/dl'
                        value={formData.chol}
                        onChange={onInputChange}
                        required
                    />

                    <label className='Patientlabel' htmlFor="fbs">Fasting Blood Sugar &gt; 120 mg/dl</label>
                    <select
                        className='Patientinput'
                        id="fbs"
                        name="fbs"
                        value={formData.fbs}
                        onChange={onInputChange}
                        required
                    >
                        <option value="" disabled>Select True or False</option>
                        <option value="1">True</option>
                        <option value="0">False</option>
                    </select>

                    <label className='Patientlabel' htmlFor="restecg">Resting Electrocardiographic Results</label>
                    <select
                        className='Patientinput'
                        id="restecg"
                        name="restecg"
                        value={formData.restecg}
                        onChange={onInputChange}
                        required
                    >
                        <option value="" disabled>Select type</option>
                        <option value="0">Normal</option>
                        <option value="1">Abnormal - ST-T wave</option>
                        <option value="2">Abnormal - Left Ventricular Hypertrophy</option>
                    </select>

                    <label className='Patientlabel' htmlFor="thalach">Maximum Heart Rate Achieved</label>
                    <input
                        className='Patientinput'
                        type="number"
                        id="thalach"
                        name="thalach"
                        value={formData.thalach}
                        onChange={onInputChange}
                        required
                        min='1'
                    />

                    <label className='Patientlabel' htmlFor="exang">Exercise Induced Angina</label>
                    <select
                        className='Patientinput'
                        id="exang"
                        name="exang"
                        value={formData.exang}
                        onChange={onInputChange}
                        required
                    >
                        <option value="" disabled>Select Yes or No</option>
                        <option value="1">Yes</option>
                        <option value="0">No</option>
                    </select>

                    <label className='Patientlabel' htmlFor="oldpeak">ST Depression</label>
                    <input
                        className='Patientinput'
                        type="number"
                        id="oldpeak"
                        name="oldpeak"
                        value={formData.oldpeak}
                        onChange={onInputChange}
                        required
                    />

                    <label className='Patientlabel' htmlFor="slope">Slope</label>
                    <select
                        className='Patientinput'
                        id="slope"
                        name="slope"
                        value={formData.slope}
                        onChange={onInputChange}
                        required
                    >
                        <option value="" disabled>Select type</option>
                        <option value="1">Upsloping</option>
                        <option value="2">Flat</option>
                        <option value="3">Downsloping</option>
                    </select>

                    <label className='Patientlabel' htmlFor="ca">Number of Major Vessels (0.0-3.0) Colored by Fluoroscopy</label>
                    <input
                        className='Patientinput'
                        type="number"
                        id="ca"
                        name="ca"
                        value={formData.ca}
                        onChange={onInputChange}
                        min="0"
                        max="3"
                        required
                    />

                    <label className='Patientlabel' htmlFor="thal">Thallium Stress Test Result</label>
                    <select
                        className='Patientinput'
                        id="thal"
                        name="thal"
                        value={formData.thal}
                        onChange={onInputChange}
                        required
                    >
                        <option value="" disabled>Select type</option>
                        <option value="3">Normal</option>
                        <option value="6">Fixed Defect</option>
                        <option value="7">Reversible Defect</option>
                    </select>

                    <label className='Section_name'>ECG Section</label>
                    <label className='Patientlabel' htmlFor="image">Upload ECG Image</label>
                    <input
                        className='Patientinput'
                        type="file"
                        id="image"
                        name="image"
                        accept="image/*"
                        onChange={onFileUpload}
                    />

                    <label className='Section_name'>Echocardiography Section</label>
                    <label className='Patientlabel' htmlFor="video">Upload Echocardiography Video</label>
                    <input
                        className='Patientinput'
                        type="file"
                        id="video"
                        name="video"
                        accept="video/*"
                        onChange={onFileUpload}
                    />
                </div>


            </form>
            {/* </div> */}
        </div>
    );
};

export default Add_Patient;
