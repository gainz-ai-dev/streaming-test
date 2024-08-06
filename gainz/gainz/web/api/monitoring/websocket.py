from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi import Depends, HTTPException, status
import os
import openai
import json
from .auth import get_current_user
from .model import User, Login, Token
from dotenv import load_dotenv

load_dotenv()
# OpenAI Key is in .env. However, it would not save in gitHub. Please send request to henry930@gmail.com, or you create your own. 
# This is the main API for openAI assistant. Currently, just use the mini one. I have charged up few credit. May be used up. Please inform henry930@gmail.com for any issues, or you create your own. 

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# The arr is the array of messages. All messages of a thread will be fed up for replies generation. 
def openChat(arr):
    msgs=[]
    for msg in arr:
        item = {"role": "assistant", "content": msg}
        msgs.append(item)
    completion = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages= msgs
    )
    return completion.choices[0].message.content

ws = APIRouter()

# This is the main websocket API for AI messages. 
# To DO: Other training, model build up, crteria checks etc. 

@ws.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        messages_array = json.loads(data)
        
        reply = openChat(messages_array)
        await websocket.send_text(reply)
