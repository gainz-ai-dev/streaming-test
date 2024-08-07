import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import { connectWebSocket } from '../utils/websocket';

import 'bootstrap/dist/css/bootstrap.min.css';

const Chat = ({ threadId }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [socket, setSocket] = useState(null);
  const [animatingMessage, setAnimatingMessage] = useState('');
  const [animatingIndex, setAnimatingIndex] = useState(0);
  const requestRef = useRef();
  const animationSpeed = 50;
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/auth/login');
    } else {
      const ws = connectWebSocket(token, (message) => {
        if (message === "done") {
          clearTimeout(requestRef.current);
          return;
        }
        setAnimatingMessage(message);
        setAnimatingIndex(0);
      }, threadId);
      setSocket(ws);

      return () => {
        ws.close();
      };
    }
  }, [threadId]);

  useEffect(() => {
    const animateMessage = () => {
      setMessages((prevMessages) => {
        const newMessages = [...prevMessages];
        if (newMessages.length === 0 || newMessages[newMessages.length - 1].sender !== 'Gainz') {
          newMessages.push({ text: '', sender: 'Gainz' });
        }
        const lastMessageIndex = newMessages.length - 1;
        if (animatingIndex < animatingMessage.length) {
          newMessages[lastMessageIndex].text = animatingMessage.substring(0, animatingIndex + 1);
          setAnimatingIndex(animatingIndex + 1);
          requestRef.current = setTimeout(animateMessage, animationSpeed);
        } else {
          clearTimeout(requestRef.current);
        }
        return newMessages;
      });
    };

    if (animatingMessage) {
      requestRef.current = setTimeout(animateMessage, animationSpeed);
    }

    return () => clearTimeout(requestRef.current);
  }, [animatingMessage, animatingIndex]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim() && socket) {
      socket.send(newMessage);
      setMessages([...messages, { text: newMessage, sender: 'You' }]);
      setNewMessage('');
    }
  };

  return (
    <Container className="chat-container pt-5">
      <Row className="justify-content-md-center">
        <Col md={8}>
          <div className="chat-header">
            <h2>Gainz Assistant</h2>
          </div>
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className="chat-message">
                <strong>{msg.sender}: </strong> {msg.text}
              </div>
            ))}
          </div>
          <Form onSubmit={handleSendMessage} className="chat-input-form">
            <Form.Group controlId="formNewMessage">
              <Form.Control
                type="text"
                placeholder="Ask a query to Gainz..."
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Send
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default Chat;
