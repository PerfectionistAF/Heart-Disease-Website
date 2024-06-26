import React, { useState, useEffect, Component } from 'react'
import { Hoome, Container, Homebtn, Homedesc, Homeinfo, Hometitle, Span } from './style.js'
import { Link, useNavigate } from 'react-router-dom';
import './Hstyle.css';
import authService from '../../authService.js';
import axios from 'axios';


const Home = ({ user }) => {
    const [patients, setPatients] = useState([]);
    const [patientFiles, setPatientFiles] = useState([]);
    const [error, setError] = useState('');

    const navigate = useNavigate();

    // const handleLogout = () => {
    //     authService.logout();
    //     navigate('/Login');
    // };

    const [currentPage, setCurrentPage] = useState(1);
    const pageSize = 5;


    const [showOptions, setShowOptions] = useState(false);
    const [selectedOption, setSelectedOption] = useState('');

    const toggleOptions = () => {
        setShowOptions(!showOptions);
    };


    const renderTable = () => {
        const start = (currentPage - 1) * pageSize;
        const end = start + pageSize;
        const paddedEnd = Math.max(end, patients.length % pageSize);
        const rows = [];

        for (let i = start; i < paddedEnd; i++) {
            if (i < patients.length) {
                rows.push(


                    <tr key={patients[i].id}>


                        <th>{patients[i].name}</th>


                        <td className='button-group'>


                            <button className='Addbutton' onClick={() => handleAdd(patients[i].id)}>Add</button>
                            <button className='Removebutton' onClick={() => handleRemove(patients[i].id)}>Remove</button>
                            <button className='Viewbutton' onClick={() => handleView(patients[i].id)}>View</button>


                        </td>

                    </tr>

                );
            }

            else {

                rows.push(
                    <tr key={i}>
                        <th className='empty'></th>
                        <td className=" empty"></td>
                    </tr>
                );
            }
        }

        return rows;
    };

    const prevPage = () => {
        if (currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
    };

    const nextPage = () => {
        const totalPages = Math.ceil(patients.length / pageSize);
        if (currentPage < totalPages) {
            setCurrentPage(currentPage + 1);
        }
    };


    const handleOptionClick = async (option) => {
        setSelectedOption(option);
        console.log("option: " + option);
        switch (option) {
            case 'PName asc':
                // Handle logic for Patients (name: ascending)
                const response = await axios.get(`${process.env.REACT_APP_API_URL}patients/?doctor=${user?.id}&ordering=name`);
                setPatients(response.data);
                break;
            case 'PName des':
                // Handle logic for Patients (name: descending)
                const response2 = await axios.get(`${process.env.REACT_APP_API_URL}patients/?doctor=${user?.id}&ordering=-name`);
                setPatients(response2.data);
                break;
            case 'PDate asc':
                // Handle logic for Patients (date: ascending)
                const response3 = await axios.get(`${process.env.REACT_APP_API_URL}patients/?doctor=${user?.id}&ordering=created_at`);
                setPatients(response3.data);
                break;
            case 'PDate des':
                // Handle logic for Patients (date: descending)
                const response4 = await axios.get(`${process.env.REACT_APP_API_URL}patients/?doctor=${user?.id}&ordering=-created_at`);
                setPatients(response4.data);
                break;
            case 'FSeverity asc':
                // Handle logic for Files (severity: high)
                const response5 = await axios.get(`${process.env.REACT_APP_API_URL}doctor-patient-files/?doctor=${user?.id}&final_diagnosis=damage`);
                const response5b = await axios.get(`${process.env.REACT_APP_API_URL}doctor-patient-files/?doctor=${user?.id}&final_diagnosis=risk`);
                const files = response5.data.concat(response5b.data); // Correctly concatenate the arrays
                const len = files.length;
                console.log(files);
                const newPatients = [];
                const encounteredPatients = new Set();

                for (let i = 0; i < len; i++) {
                    console.log("files[i].patient: " + files[i].patient);
                    if (!encounteredPatients.has(files[i].patient)) {
                        const response6 = await axios.get(`${process.env.REACT_APP_API_URL}patients/${files[i].patient}`);
                        newPatients.push(response6.data);
                        encounteredPatients.add(files[i].patient);
                        console.log("response 6: ", response6);
                    } else {
                        console.log(`Patient ${files[i].patient} is duplicated. Skipping.`);
                    }
                }

                setPatients(newPatients);
                break;
            case 'FSeverity des':
                // Handle logic for Files (severity: low)
                const response7 = await axios.get(`${process.env.REACT_APP_API_URL}doctor-patient-files/?doctor=${user?.id}&final_diagnosis=healthy`);
                console.log(response7.data);
                const len2 = response7.data.length;
                const files2 = response7.data;
                const newPatients2 = [];
                const encounteredPatients2 = new Set();

                for (let i = 0; i < len2; i++) {
                    console.log("files2[i].patient: " + files2[i].patient);
                    if (!encounteredPatients2.has(files2[i].patient)) {
                        const response8 = await axios.get(`${process.env.REACT_APP_API_URL}patients/${files2[i].patient}`);
                        newPatients2.push(response8.data);
                        encounteredPatients2.add(files2[i].patient);
                        console.log("response 8: ", response8);
                    } else {
                        console.log(`Patient ${files2[i].patient} is duplicated. Skipping.`);
                    }
                }

                setPatients(newPatients2);
                break;
            // case 'Fdate asc':
            //     // Handle logic for Files (date: ascending)
            //     break;
            // case 'Fdate des':
            //     // Handle logic for Files (date: descending)
            //     break;
            default:
                // Default case if none of the options match
                break;
        }

        setShowOptions(false);
    };



    useEffect(() => {
        const fetchPatients = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_API_URL}patients/?name=&doctor=${user?.id}&created_at_after=&created_at_before=`);
                setPatients(response.data);
            } catch (error) {
                setError('There was an error fetching the patients');
                console.error('Error fetching patients:', error);
            }
        };

        // const fetchPatientFiles = async () => {
        //     try {
        //         const response = await axios.get(`${process.env.REACT_APP_API_URL}doctor-patient-files/?name=&doctor=${user?.id}`);
        //         setPatientFiles(response.data);
        //     } catch (error) {
        //         setError('There was an error fetching the patients');
        //         console.error('Error fetching patients:', error);
        //     }
        // };

        fetchPatients();
        // fetchPatientFiles();
    }, []);

    const handleAdd = (patientId) => {
        console.log('Add patient with ID:', patientId);
        navigate('/Add_Patient/' + patientId);
    };


    const handleView = (patientId) => {
        navigate('/View', { state: { patientId } });
        console.log("Viewing... " + patientId);
    }

    const handleRemove = async (patientId) => {
        console.log("Removing... " + patientId);
        try {
            const response = await axios.delete(`${process.env.REACT_APP_API_URL}patients/${patientId}/`);
            if (response.status === 204) {
                console.log('Successfully deleted');
                setPatients(patients.filter(patient => patient.id !== patientId));
            } else {
                console.log('Failed to delete');
            }
        } catch (error) {
            console.error('There was an error deleting the patient:', error);
        }
    }

    return (
        <div>

            <Hoome>
                <Container>
                    <Hometitle> Hello, Dr. {user.first_name}</Hometitle>
                    <div className='Filter_container'>
                        <div className="iconContainer">
                            <i className="fa fa-sort Ic" onClick={toggleOptions}> Sort</i>
                            {/* <i className="fa fa-filter Ic"  > Filter</i> */}
                        </div>



                        {showOptions && (
                            <table className="options-list">
                                <td className='option' onClick={() => handleOptionClick('PName asc')}>Patients (name: ascending)</td>
                                <td className='option' onClick={() => handleOptionClick('PName des')}>Patients (name: descending)</td>
                                <td className='option' onClick={() => handleOptionClick('PDate asc')}>Patients (date: ascending)</td>
                                <td className='option' onClick={() => handleOptionClick('PDate des')}>Patients (date: descending)</td>
                                <td className='option' onClick={() => handleOptionClick('FSeverity asc')}>Files (severity: high)</td>
                                <td className='option' onClick={() => handleOptionClick('FSeverity des')}>Files (severity: low)</td>
                                {/* <td className='option' onClick={() => handleOptionClick('Fdate asc')}>Files (date: ascending)</td>
                                <td className='option' onClick={() => handleOptionClick('Fdate des')}>Files (date: descending)</td> */}
                            </table>
                        )}
                        {error && <p style={{ color: 'red' }}>{error}</p>}



                        <>

                            <table className='main-table'>
                                <thead>
                                    <tr >
                                        <th colSpan="4" className='table-name'>Patient List</th>
                                    </tr >
                                </thead>
                                {patients.length > 0 ? (
                                    <tbody>


                                        {renderTable()}
                                    </tbody>
                                ) : (
                                    <tbody>
                                        <tr id='Nopa'> No patients found</tr>
                                    </tbody>

                                )}
                            </table>
                        </>




                        <div className="button-group2">
                            <button className="prev-button" onClick={prevPage}>Previous</button>
                            <button className="next-button" onClick={nextPage}>Next</button>
                        </div>


                        <Link to='/New_Patient'>
                            <button className='Newbutton'>
                                New Patient
                            </button>
                        </Link>


                        {/* <button className='Log out' onClick={handleLogout}>
                            Log out
                        </button> */}

                    </div>
                </Container>
            </Hoome>
        </div >
    );
};

export default Home;
