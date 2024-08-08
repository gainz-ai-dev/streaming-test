import { useState, useEffect, useRef } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { TextField,Button,ButtonGroup,IconButton,List,ListItemButton,ListItemIcon,ListItemText} from '@mui/material';
import { createSvgIcon } from '@mui/material/utils';
import ListIcon from '@mui/icons-material/List';
import { HiChevronDoubleRight } from "react-icons/hi";

import axios from 'axios';  

const PlusIcon = createSvgIcon(
  // credit: plus icon from https://heroicons.com/
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    strokeWidth={1.5}
    stroke="currentColor"
  >
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
  </svg>,
  'Plus',
);

const _URL = "http://127.0.0.1:8000"

interface Message {
    sender: string, 
    message: string
}
interface Thread_Message{
    tid: string, 
    message: string
}
function messsageRenderer(msg:String){
    msg = msg.replace(/\n/g, '<br>')
    msg= msg.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
    return msg
}

// This is the main chatroom component. WebSocket will be connected. Please ensure the local backend has been kickstarted.
// the socketUrl is hardcode. Will setup a testing server for this in future. 

function WebSocket() {
  const [message, setMessage] = useState('');
  const [msg,setMsg] = useState<Message[]>([])
  const [threadId, setThreadId] = useState('')
  const token = localStorage.getItem('access_token') || null;
  const socketUrl = `ws://localhost:8000/api/ws` // Replace with your WebSocket server URL

  const [windowHeight, setWindowHeight] = useState(window.innerHeight);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    setTimeout(() => {
        if (messagesEndRef.current)
            messagesEndRef.current.scrollTop = messagesEndRef.current.scrollHeight;
    }, 100); 
    
  };
 
  useEffect(() => {
    const handleResize = () => {
      setWindowHeight(window.innerHeight*0.8);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const {
    sendMessage,
    sendJsonMessage,
    lastMessage,
    readyState,
  } = useWebSocket(socketUrl);

  useEffect(() => {
    if (readyState === ReadyState.OPEN) {
        // This is for token authentication in API level. Currently, we just have authentication in html rendering level. 
        console.log('WebSocket connected');
    }
  }, [sendMessage, readyState, token]);

  useEffect(() => {
    if (lastMessage) {
      console.log(lastMessage)
      
        // let item:Message= {
        //     sender:'',
        //     message:''
        // }
        // item['sender'] = "ai"
        // item['message'] = lastMessage.data
        // let arr = [...msg, ...[item]]
        // setMsg(arr) 
        // scrollToBottom()       
    }
  }, [lastMessage]);

  const handleNewThread = async () => { 
    try {
      const response = await axios.post(_URL+'/api/create-thread',{
      }, {
          headers:{
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
          }
      })
      console.log('Messages',response)
    } catch (error) {
      console.log(error)
    }
    setMsg([])
    setMessage('')
    scrollToBottom()
  };

  const handleListThread=()=>{

  }
  const handleRun=()=>{

  }
  const handleSendMessage = () => {
    let arr1:String[] =[];
    msg.forEach(item=>{
        if (item.sender=="me")
            arr1.push(item.message)
    });
    arr1.push(message)

    // Old Method
    // sendMessage(JSON.stringify(arr1))

    // New Method
    let json: Thread_Message
    json ={
       'tid': threadId, 
       'message': message
    }
    sendMessage(JSON.stringify(json))

    let item:Message= {
        sender:'',
        message:''
    }
    item['sender'] = "me"
    item['message'] = message
    let arr = [...msg, ...[item]]
    setMsg(arr)
    setMessage('')
    scrollToBottom()
  };

  return (
    <div className="panel">
      <div className="toolbar">

      <List component="nav" aria-label="main mailbox folders">
        <ListItemButton
          selected
        >
          <ListItemIcon>
            <ListIcon />
          </ListItemIcon>
          <ListItemText primary="Inbox" />
        </ListItemButton>
        <ListItemButton>
          <ListItemIcon>
            <ListIcon />
          </ListItemIcon>
          <ListItemText primary="Drafts" />
        </ListItemButton>
      </List>
      <ButtonGroup orientation="horizontal" aria-label="Vertical button group">
            <IconButton onClick={handleNewThread} aria-label="New Thread">
              <PlusIcon />
            </IconButton>
            <IconButton onClick={handleRun} color="secondary" aria-label="Run">
              <HiChevronDoubleRight />
            </IconButton>
        </ButtonGroup>

      </div>
      <div className="chat-container" style={{ height: `${windowHeight}px` }}>
          <div className="chat-messages"  ref={messagesEndRef} >
              {msg.map((item, index) => (
                  <div key={index} className={item.sender}>
                      <p dangerouslySetInnerHTML={{ __html: String(messsageRenderer(item.message)) }}></p>
                  </div>
              ))} 
              <div ref={messagesEndRef} />
          </div>
          <div className="chat-input">
              <TextField type="text" id="message-input" variant="standard"  placeholder="Type your message" value={message} onChange={(e) => setMessage(e.target.value)} />
              <Button id="send-button" className="button" onClick={handleSendMessage}>Send</Button>
          </div>
      </div>
    </div>

  );
}

export default WebSocket;
