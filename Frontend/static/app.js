

let socket;
let threadId;
let recognition;
let isRecognizing = false;


async function initializeConversation() {
    try {
        const response = await fetch("/initialize", { 
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Initialization response:", data);
        return data.thread_id;
    } catch (error) {
        console.error("Error initializing conversation:", error);
    }
}


async function connect() {
    try {
        threadId = await initializeConversation();

        

        socket = new WebSocket(`ws://127.0.0.1:8000/ws/${threadId}`);

        socket.onopen = () => console.log("Connected to the server");
        socket.onclose = () => alert("Disconnected from the server.");
        socket.onerror = (error) => alert(`WebSocket error: ${error.message}`);
        socket.onmessage = handleMessage;

        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onresult = (event) => {
                document.getElementById("message").value = event.results[0][0].transcript;
            };

            recognition.onerror = (event) => console.error("Speech recognition error:", event.error);
            recognition.onend = () => {
                console.log("Speech recognition ended.");
                isRecognizing = false;
                updateMicButton();
            };
        } else {
            alert("Speech recognition is not supported in this browser.");
            

        }
        updateDateTime();
    } catch (error) {
        console.error("Connection error:", error);
        alert("Error connecting to WebSocket.");
    }
}




function toggleRecognition() {
    if (recognition) {
        if (isRecognizing) {
            recognition.stop();
        } else {
            recognition.start();
        }
        isRecognizing = !isRecognizing;
        updateMicButton();
    } else {
        alert("Speech recognition is not supported.");
    }
}

function updateMicButton() {
    const micButton = document.getElementById("mic-button");
    micButton.classList.toggle("active", isRecognizing);
    micButton.innerText = isRecognizing ? "🛑" : "🎤";
}

function sendMessage() {
    if (socket && socket.readyState === WebSocket.OPEN) {
        const message = document.getElementById("message").value;
        if (message.trim() === "") return;
        socket.send(message);
        displayMessage('user', message);
        document.getElementById("message").value = ''; 
    } else {
        alert("WebSocket is not open.");
    }
}

function displayMessage(role, message) {
    const messagesElement = document.getElementById("messages");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");

    const timestamp = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

    if (role === 'user') {
        messageElement.classList.add("user-message");
        messageElement.innerHTML = `
            <div class="message-content">
                <strong>You:</strong> ${message}
            </div>
            <div class="timestamp">${timestamp}</div>
        `;
    } else {
        messageElement.classList.add("assistant-message");
        messageElement.innerHTML = `
            <div class="message-content">
                <strong>Assistant:</strong> ${message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\n/g, '<br>')
                    .replace(/: /g, ':<br>&nbsp;&nbsp;&nbsp;&nbsp;')}
            </div>
            <div class="timestamp">${timestamp}</div>
        `;
    }

    messagesElement.appendChild(messageElement);
    messagesElement.scrollTop = messagesElement.scrollHeight;  
}

function escapeHtml(unsafe) {
    return unsafe.replace(/[&<"']/g, function (m) {
        switch (m) {
            case '&': return '&amp;';
            case '<': return '&lt;';
            case '"': return '&quot;';
            case "'": return '&#039;';
            default: return m;
        }
    });
}

function handleMessage(event) {
    console.log("Message received:", event.data);

    try {
        // Log the event data to see what it contains
        console.log("Raw event data:", event.data);

        // Attempt to parse or handle the message data
        const escapedMessage = event.data || "No response data";
        const  message= escapeHtml(escapedMessage);


        message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                  .replace(/\n/g, '<br>')
                  .replace(/: /g, ':<br>&nbsp;&nbsp;&nbsp;&nbsp;');

        // Log the message to see its value
        console.log("Parsed message:", message);

        // Display the message
        displayMessage('assistant', message);
    } catch (error) {
        console.error("Error parsing message:", error);
    }
}


function updateDateTime() {
    const dateTimeElement = document.getElementById('date-time');
    const update = () => {
        const now = new Date();
        dateTimeElement.textContent = now.toLocaleString('en-US', {
            weekday: 'short',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };
    update();
    setInterval(update, 60000); 
}
window.onload = connect;
