// import React from 'react';
// import { Navigate } from 'react-router-dom';

// const ProtectedRoute = ({ component: Component }) => {
//     const user = JSON.parse(localStorage.getItem('user'));
//     if (!user || !user.access) {
//         return <Navigate to="/Login" />;
//     }
//     return <Component />;
// };

// export default ProtectedRoute;



import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ element }) => {
    const isAuthenticated = localStorage.getItem('access') !== null;
    const user = JSON.parse(localStorage.getItem('user'));

    return isAuthenticated ? React.cloneElement(element, { user }) : <Navigate to="/Login" />;
};

export default ProtectedRoute;

