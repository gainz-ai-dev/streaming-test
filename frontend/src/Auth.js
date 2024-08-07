import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { verifyToken } from '../network/ApiAxios';

export function Auth(WrappedComponent) {
    return function WithAuthentication(props) {
        const [isAuthenticated, setIsAuthenticated] = useState(false);
        const navigate = useNavigate();

        useEffect(() => {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/auth/login');
            } else {
                verifyToken(token).then(response => {
                    if (response.success) {
                        setIsAuthenticated(true);
                    } else {
                        localStorage.removeItem('token');
                        navigate('/auth/login');
                    }
                }).catch(() => {
                    localStorage.removeItem('token');
                    navigate('/auth/login');
                });
            }
        }, [navigate]);

        if (!isAuthenticated) {
            return <div></div>;
        }

        return <WrappedComponent {...props} />;
    };
}
