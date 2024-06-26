import React from 'react';
import './style.css';

const New_Patient = ({ formData, onInputChange }) => {
    return (
        <div >
            <form className='Patientform' id='Patientdataform'>
                <label className='Section_name' id='newlabel'> Personal Information</label>
                <label className='Patientlabel' htmlFor="NPatientname">Name</label>
                <input
                    className='Patientinput pp'
                    type="text"
                    id="NPatientname"
                    name="name"
                    placeholder='Patient Name'
                    value={formData.name}
                    onChange={onInputChange}
                    required
                />
                <label className='Patientlabel' htmlFor="NPatientnumber">Phone Number</label>
                <input
                    className='Patientinput pp'
                    type="tel"
                    id="NPatientnumber"
                    name="phone_number"
                    placeholder='Patient Phone Number'
                    value={formData.phone_number}
                    onChange={onInputChange}
                    required
                />
                <label className='Patientlabel' htmlFor="Nbirthdate">Birthdate</label>
                <input
                    className='Patientinput pp'
                    type="date"
                    id="Nbirthdate"
                    name="birthdate"
                    placeholder='Patient Birthdate'
                    value={formData.birthdate}
                    onChange={onInputChange}
                    required
                />
                <label className='Patientlabel' htmlFor="NPatientAddress">Address</label>
                <input
                    className='Patientinput pp'
                    type="text"
                    id="NPatientAddress"
                    name="address"
                    placeholder='Patient Address'
                    value={formData.address}
                    onChange={onInputChange}
                    required
                />


            </form>
        </div>
    );
};

export default New_Patient;
