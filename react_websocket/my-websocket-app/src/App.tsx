import Login from './Login'
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import './App.css';

function App() {
    return (
      <div className="App">
        <CssBaseline />
        <Container maxWidth="md">
          <Box sx={{ bgcolor: '#cfe8fc', height: '100vh' }} >
            <Login />        
          </Box>
        </Container>
        <header className="App-header">

        </header>
      </div>      
    )
}

export default App;
