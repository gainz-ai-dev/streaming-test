import { useState, useEffect, useRef } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import { TextField,Button } from '@mui/material';
  
interface Message {
    sender: string, 
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

  const handleNewThread = () => { 
    setMsg([])
    setMessage('')
    scrollToBottom()
  };

  const handleSendMessage = () => {
    let arr1:String[] =[];
    msg.forEach(item=>{
        if (item.sender=="me")
            arr1.push(item.message)
    });
    arr1.push(message)
    sendMessage(JSON.stringify(arr1))
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
            <Button id="send-button" onClick={handleNewThread}>New Thread</Button>
            <TextField type="text" id="message-input" variant="standard"  placeholder="Type your message" value={message} onChange={(e) => setMessage(e.target.value)} />
            <Button id="send-button" onClick={handleSendMessage}>Send</Button>
        </div>
    </div>
  );
}

export default WebSocket;
