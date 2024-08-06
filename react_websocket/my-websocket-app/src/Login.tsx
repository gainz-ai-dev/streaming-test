import { useState, useEffect } from 'react';
import axios from 'axios';
import WebSocket from './webSocket';
import CssBaseline from '@mui/material/CssBaseline';
import { TextField, Button, ButtonGroup } from '@mui/material';

// URL has been hard code. Definitely not good, due to time constrint. 
// To Do: will setup a testing API server, instead of local one. 
let _URL = "http://127.0.0.1:8000"

const Login = () => {
  // logined is for determinating showing the chatroom or login page
  const [logined, setLogin] = useState(false);
  // name, email, password, repassword are variables for login/ register
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repassword, setRePassword] = useState('');
  // isRegister is to show login page or register page
  const [isRegister, setIsRegister] = useState(false);
  // error Message for telling users the status and instruction. 
  const [errorMsg, setErrorMsg] = useState('');
  // JWT token are local stored for checking the permission of further works. 
  // To DO: Need to turn the authentication API-wise, instead of checking only at start. 
  const token =localStorage.getItem('access_token') || null;
  const checkPassword= () =>{
    if (password === repassword) {
      setErrorMsg("")
      return true;
    }
    else {
      setErrorMsg("Your password and retype password do not match")
      return false;
    }
  }
  useEffect( () => {
    const fetchData = async () => {
        console.log('Token',token)
        if (token) {
            try {
                const response = await axios.post(_URL+'/api/protected_route', {
                }, {
                    headers:{
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`
                    }
                })
                console.log(response);
                if (response.data)
                    setLogin(true);
                else
                    setLogin(false);
                // Handle successful login, store access token
            } catch (error) {
                setLogin(false);
            }
        } else
            setLogin(false);
      };
      fetchData();
  }, [token]);
  const handleRegister = async (e:any) => {
    e.preventDefault();
    if (isRegister && checkPassword()) {
      try {
        const response = await axios.post(_URL+'/api/register', {
          'id':email,
          'name':name,
          'email':email,
          'password':password,
        });
        if (response)
            setErrorMsg("Your account register successfully. Please click login for our AI chatbot");
      } catch (error) {
        setErrorMsg("Your account register unsuccessfully. May be your email has been registered before.");
        console.error(error);
        // Handle login error
      }      
    }
    setIsRegister(true)
  }
  const handleSubmit = async (e:any) => {
    e.preventDefault();
    if (!isRegister) {
      try {
        const response = await axios.post(_URL+'/api/login', {
          email,
          password,
        });
        if (response.data.access_token) {
          // When login success, token will be stored. 
          localStorage.setItem('access_token', response.data.access_token);
          setLogin(true);
        }
        console.log(response.data);
        // Handle successful login, store access token
      } catch (error) {
        console.error(error);
        // Handle login error
      }      
    }
    setIsRegister(false)

  };
  const logout = ()=>{
    // When logout, token will be removed.
    localStorage.removeItem('access_token');     
    setLogin(false);   
  }
  if (logined)
    return (
        <div className="wrapper">
          <Button variant="contained" className="logout" onClick={logout}>Logout</Button>
          <WebSocket />
        </div>       
    )
  else
    return (
        <div className="login-wrapper">
          <div className="footer__company">
            <img src="https://www.gainz.ai/assets/icons/logo.svg" alt="logo" className="footer__company-logo" />
            <p className="footer__company-text">© 2024 Gainz AI</p>
          </div>
          
          {
            isRegister? (
              <div className="register-section">
                <TextField id="outlined-basic" label="Name" variant="outlined" type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)}/>
                <TextField id="outlined-basic" label="Email" variant="outlined" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}/>
                <TextField id="outlined-basic" label="Password" variant="outlined" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}/>
                <TextField id="outlined-basic" label="Retype Password" variant="outlined" type="password" placeholder="Retype Password" value={repassword} onChange={(e) => setRePassword(e.target.value)}/>
                <div className="button-group"> 
                  <Button onClick={handleRegister} variant="contained">Register</Button>
                  <Button onClick={handleSubmit} variant="outlined">Login</Button>
                </div>
                <div className="error-message">{errorMsg}</div>
              </div>
            ) : (
              <div className="login-section">
                <TextField id="outlined-basic" label="Email" variant="outlined" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}/>
                <TextField id="outlined-basic" label="Password" variant="outlined" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}/>
                <div className="button-group"> 
                  <Button onClick={handleSubmit} variant="contained">Login</Button>
                  <Button onClick={handleRegister} variant="outlined">Register</Button>
                </div>
                <div className="error-message">{errorMsg}</div>
              </div>
            )
          }

          <div className="footer"></div>
        </div>
    );
};

export default Login;
