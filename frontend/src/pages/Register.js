import React, { useState } from 'react';
import { Link } from "react-router-dom";
import { Container, Row, Col, Form, Button, Card, Alert } from 'react-bootstrap';

import { register } from '../utils/api';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [termsAccepted, setTermsAccepted] = useState(false);
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    let newErrors = {};
    if (!email.trim()) {
      newErrors.email = "Email is required.";
    }
    if (!password.trim()) {
      newErrors.password = "Password is required.";
    }
    if (!termsAccepted) {
      newErrors.terms = "You must agree to the terms and conditions to register.";
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      const data = await register(email, password);
      if (data.success) {
        setErrors({});
        setSuccess(true);
      } else {
        setErrors({ form: data.message });
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
                  <h2 className='mb-5'>Register</h2>
                  {errors.form && <Alert variant="danger">{errors.form}</Alert>}
                  {success && <Alert variant="success">Registration successful!</Alert>}

                  <Form onSubmit={handleRegister}>
                    <Form.Group controlId="formBasicEmail" className='mb-4'>
                      <Form.Label className='text-start d-block'>Email address</Form.Label>
                      <Form.Control
                        type="email"
                        placeholder="Enter email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                      />
                      {errors.email && <small className="text-danger">{errors.email}</small>}
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

                    <Form.Group controlId="formBasicCheckbox" className='mb-4'>
                      <Form.Check
                        type="checkbox"
                        label="I agree to the terms and conditions"
                        checked={termsAccepted}
                        onChange={(e) => setTermsAccepted(e.target.checked)}
                      />
                      {errors.terms && <small className="text-danger">{errors.terms}</small>}
                    </Form.Group>

                    <Button variant="primary" type="submit">
                      Register
                    </Button>
                  </Form>
                  <div className="mt-3">
                    <Link to="/auth/login" className="App-link">
                      Already have an account? Login here
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

export default Register;
