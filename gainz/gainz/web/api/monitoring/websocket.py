from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi import Depends, HTTPException, status
import os
from openai import OpenAI
import json
from .auth import get_current_user
from .model import User, Login, Token, Message, Thread
from .db import create_message_record, create_thread_record
import time
from dotenv import load_dotenv

load_dotenv()
# OpenAI Key is in .env. However, it would not save in gitHub. Please send request to henry930@gmail.com, or you create your own. 
# This is the main API for openAI assistant. Currently, just use the mini one. I have charged up few credit. May be used up. Please inform henry930@gmail.com for any issues, or you create your own. 
# For convinence, all demo are using same assistant for test. When user registered, will have an assistant created for him. 

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# openai.api_key = OPENAI_API_KEY
ASSISTANT_ID = 'asst_3N9bkD5CyXgT5O9T9J3n8AIW'
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
threadId = ''
# The arr is the array of messages. All messages of a thread will be fed up for replies generation. 
def openChat(arr):
    msgs=[]
    for msg in arr:
        item = {"role": "assistant", "content": msg}
        msgs.append(item)
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages= msgs
    )
    return completion.choices[0].message.content

def chatAssistantCreate():
    assistant = client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor. Answer questions briefly, in a sentence or less.",
        model="gpt-4o-mini",
    )
    return assistant

def chatCreateMessage(tid: str,msg: str):

    message = client.beta.threads.messages.create(
        thread_id=str(tid),
        role="user",
        content=str(msg)
    )
    return message

def chatListMessages(thread_id:str):
    messages = client.beta.threads.messages.list(thread_id=thread_id, order="asc")
    return messages

def chatThreadRun(thread_id:str,assistant_id:str):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    return run

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    # run = submit_message(MATH_ASSISTANT_ID, thread, user_input)
    # return thread, run

ws = APIRouter()

# This is the main websocket API for AI messages. 
# To DO: Other training, model build up, crteria checks etc. 

@ws.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global threadId
    await websocket.accept()
    thread = client.beta.threads.create()
    tid = thread.id
    threadId = thread.id
    print(tid)
    while True:
        data = await websocket.receive_text()
        ### This is old method 
        # messages_array = json.loads(data)        
        # reply = openChat(messages_array)
        
        # New method
        messages_array = json.loads(data)
        print(messages_array)
        response = chatCreateMessage(tid,messages_array['message'])
        await websocket.send_text(response)


@ws.post("/create-assistant")
async def create_assistant():
    return {"message":"Assistant created successfully."}

@ws.post("/create-message")
async def chatCreateMessage(ms:Message):
    thread = chatCreateMessage(ms.tid,ms.msg)
    print(thread)
    return thread



@ws.post("/create-thread")
async def chatCreateThread(current_user: User = Depends(get_current_user)):
    response = client.beta.threads.create()
    try:
        thread_data = {
            "id": response.id,
            "aid": ASSISTANT_ID,
            "uid": current_user['id'],
            "timestamp": int(time.time())
        }
        thread = Thread(**thread_data)
        create_thread_record(thread)
        return {"message":"Create Success","code": 100}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "Create fail", "code": -100}

@ws.post("/list-thread")
def chatListMessages():
    global threadId
    print(threadId)
    messages={"message":"nothing"}
    messages = client.beta.threads.messages.list(thread_id=threadId, order="asc")
    return messages

