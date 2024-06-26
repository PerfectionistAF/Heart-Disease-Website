import axios from 'axios';




const register = (formData) => {
    return axios.post(`${process.env.REACT_APP_API_URL}register/`, formData, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
};



const login = async (email, password) => {
    const response = await axios.post(`${process.env.REACT_APP_API_URL}login/`, { email, password }, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
    if (response.data.access) {
        localStorage.setItem('user', JSON.stringify(response.data.user));
        localStorage.setItem('access', response.data.access);
        localStorage.setItem('refresh', response.data.refresh);
    }
    return response.data;
};

const logout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
};

export default {
    register,
    login,
    logout
};
