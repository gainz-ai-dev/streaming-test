import { useState, useEffect, useRef } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { TextField,Button,ButtonGroup,IconButton,List,ListItemButton,ListItemIcon,ListItemText} from '@mui/material';
import { createSvgIcon } from '@mui/material/utils';
import ListIcon from '@mui/icons-material/List';
import DeleteIcon from '@mui/icons-material/Delete';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
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
const OPENAI_API_KEY = process.env.OPENAI_API_KEY
const ASSISTANT_ID = process.env.ASSISTANT_ID

interface Message {
    sender: string, 
    message: string
}
interface Thread {
    id: string, 
    aid: string, 
    name: string,
    timestamp: number
}
interface Thread_Message{
    id: string,
    tid: string, 
    message: string,
    timestamp: number
}
function messsageRenderer(msg:String){
    msg = msg.replace(/\n/g, '<br>')
    msg= msg.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
    return msg
}

// This is the main chatroom component. WebSocket will be connected. Please ensure the local backend has been kickstarted.
// the socketUrl is hardcode. Will setup a testing server for this in future. 

function WebSocket() {
  const [selectedItemId, setSelectedItemId] = useState<number>(0);
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [threads,setThreads] = useState<Thread[]>([])
  const [msg,setMsg] = useState<Message[]>([])
  const [threadId, setThreadId] = useState('')
  const token = localStorage.getItem('access_token') || null;
  const socketUrl = `ws://localhost:8000/api/ws` // Replace with your WebSocket server URL

  const [windowHeight, setWindowHeight] = useState(window.innerHeight);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

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
    sendJsonMessage,
    lastMessage,
    readyState,
  } = useWebSocket(socketUrl);

  useEffect(() => {

    if (readyState === ReadyState.OPEN) {
        // This is for token authentication in API level. Currently, we just have authentication in html rendering level. 
        console.log('WebSocket connected');
        handleListThread()

    }
  }, [sendJsonMessage,readyState, token]);

  useEffect(() => {
    if (lastMessage) {
      
        let item:Message= {
            sender:'',
            message:''
        }
        item['sender'] = "ai"
        item['message'] = lastMessage.data
        let arr = [...msg, ...[item]]
        setMsg(arr) 
        scrollToBottom()       
    }
  }, [lastMessage]);

  const handleNewThread = async () => { 
    // let thread_title = prompt("Please type the thread name.")
    try {
      const response = await axios.post(_URL+'/api/create-thread',{
      }, {
          headers:{
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
          }
      })
      alert('New Thread has been created. Please add some messages for AI learning. First word of your sentence will be the name the thread. You can always click the RUN button on the left side to view the result. Enjoy!')
    } catch (error) {
      console.log(error)
    }
    setMsg([])
    setMessage('')
    scrollToBottom()
  };

  const handleListMessages = async(tid:string) =>{
    try {
      console.log(tid)
      const response = await axios.post(_URL+'/api/list-messages',{
          'tid':tid
      })
      console.log(response)
    } catch (error) {
      console.log(error)
    }
  }
  const handleListThread = async ()=>{
    console.log('List Thread')
    try {
      const response = await axios.post(_URL+'/api/list-thread',{
      }, {
          headers:{
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
          }
      })
      console.log(response.data)
      let data = response?.data || [] 
      setThreads(data)
      // return response
    } catch (error) {
      console.log('No List')
      alert('No Threads we have. You may create one.')
      // return []
    }
  }
  const handleList = async ()=>{
    let message = "List all run queue list."
    let arr1:String[] =[];
    msg.forEach(item=>{
        if (item.sender=="me")
            arr1.push(item.message)
    });
    arr1.push(message)

    let threadId = threads[selectedItemId].id
    try {
      const response = await axios.post(
        `https://api.openai.com/v1/threads/${threadId}/runs`, {
          headers:{
              'Content-Type': 'application/json',
              Authorization: `Bearer ${OPENAI_API_KEY}`,
              "OpenAI-Beta": 'assistants=v2'
          }
      })
      console.log(response)
      // let data = response?.data || [] 
      // return response
    } catch (error) {
      console.log('No List')
      // return []
    }

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
  }
  const handleRun=()=>{
    let message = "Please answer based on my previous messages."
    let arr1:String[] =[];
    msg.forEach(item=>{
        if (item.sender=="me")
            arr1.push(item.message)
    });
    arr1.push(message)

    // Old Method
    // sendMessage(JSON.stringify(arr1))

    // New Method
    let threadId = threads[selectedItemId].id
    let json: Thread_Message
    json ={
       'id': 'answer', // This is for notice openAI answer the question. 
       'tid': threadId, 
       'message': message,
       'timestamp': 123445546 // Dummy the message timestamp are from the server
    }
    sendJsonMessage(json)
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
  }
  const handleDeleteAllThreads= async ()=>{
    setOpen(false)
    try {
      const response = await axios.post(_URL+'/api/delete-thread',{
      }, {
          headers:{
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
          }
      })
      console.log('Messages',response)  
      alert('All Threads Deleted.')
    } catch (error) {
      console.log(error)
      alert('Delete Unsuccessfully.')
    }
  }
  
  const handleSendMessage = async() => {
    let arr1:String[] =[];
    msg.forEach(item=>{
        if (item.sender=="me")
            arr1.push(item.message)
    });
    arr1.push(message)

    // Old Method
    // sendMessage(JSON.stringify(arr1))

    // New Method
    let threadId = threads[selectedItemId].id
    let json: Thread_Message
    json ={
       'id': 'question',
       'tid': threadId, 
       'message': message,
       'timestamp': 123445546
    }
    sendJsonMessage(json)
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
     <Dialog
        open={open}
        keepMounted
        onClose={handleClose}
        aria-describedby="alert-dialog-slide-description"
      >
        <DialogTitle>{"Alert!"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-slide-description">
            All Threads will be deleted. Do you confirm it?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Disagree</Button>
          <Button onClick={handleDeleteAllThreads}>Agree</Button>
        </DialogActions>
      </Dialog>
      <div className="toolbar">

      <List component="nav" aria-label="main mailbox folders">
          {threads.map((item,index) => (
            <ListItemButton onClick={() => {handleListMessages(item.id); setSelectedItemId(index);}
            } key={item.id} selected={index === selectedItemId}>
              <ListItemIcon>
                <ListIcon />
              </ListItemIcon>
              <ListItemText primary={"Thread "+index} />
            </ListItemButton>
          ))} 
      </List>
      <ButtonGroup orientation="horizontal" aria-label="Vertical button group">
            <IconButton onClick={handleNewThread} aria-label="New Thread">
              <PlusIcon />
            </IconButton>
            <IconButton onClick={handleList} aria-label="List Thread">
              <ListIcon />
            </IconButton>
            <IconButton onClick={handleClickOpen} aria-label="Delete Threads">
              <DeleteIcon />
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
