import React from 'react';
import { Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { logout } from '../utils/Api';

const LogoutButton = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        await logout(token);
        localStorage.removeItem('token');
        navigate('/auth/login');
      } catch (error) {
        console.error("Logout failed:", error.message);
        // Optionally display an error message to the user
      }
    } else {
      localStorage.removeItem('token');
      navigate('/auth/login');
    }
  };

  return (
    <Button variant="danger" onClick={handleLogout}>
      Logout
    </Button>
  );
};

export default LogoutButton;
