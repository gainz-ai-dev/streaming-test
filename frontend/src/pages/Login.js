import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from "react-router-dom";
import { Container, Row, Col, Form, Button, Card, Alert } from 'react-bootstrap';

import { login } from '../utils/api';
import 'bootstrap/dist/css/bootstrap.min.css';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/auth/login');
    } else {
      navigate('/');
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    let newErrors = {};
    if (!username.trim()) {
      newErrors.username = "Username is required.";
    }
    if (!password.trim()) {
      newErrors.password = "Password is required.";
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      try {
        const data = await login(username, password);
        setErrors({});
        setSuccess(true);
        localStorage.setItem('token', data.access_token);
        navigate('/');
      } catch (error) {
        setErrors({ form: 'Login failed. Please check your credentials and try again.' });
        setSuccess(false);
      }
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <Container className="pt-5">
          <Row className="justify-content-md-center">
            <Col md={5}>
              <Card>
                <Card.Body className='py-5 px-4'>
                  <h2 className='mb-5'>Login</h2>
                  {errors.form && <Alert variant="danger">{errors.form}</Alert>}
                  {success && <Alert variant="success">Login successful!</Alert>}

                  <Form onSubmit={handleLogin}>
                    <Form.Group controlId="formBasicUsername" className='mb-4'>
                      <Form.Label className='text-start d-block'>Username</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="Enter username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                      />
                      {errors.username && <small className="text-danger">{errors.username}</small>}
                    </Form.Group>

                    <Form.Group controlId="formBasicPassword" className='mb-4'>
                      <Form.Label className='text-start d-block'>Password</Form.Label>
                      <Form.Control
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                      />
                      {errors.password && <small className="text-danger">{errors.password}</small>}
                    </Form.Group>

                    <Button variant="primary" type="submit">
                      Submit
                    </Button>
                  </Form>
                  <div className="mt-3">
                    <Link to="/auth/register" className="App-link">
                      Don't have an account? Register here
                    </Link>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </header>
    </div>
  );
}

export default Login;
