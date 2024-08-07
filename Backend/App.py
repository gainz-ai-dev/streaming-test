from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect,Request,Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from Chatbot.openapi import get_response , assistant_id
import asyncio
import logging
from fastapi.staticfiles import StaticFiles
from typing import Dict, List
import os
from dotenv import load_dotenv
from auth import authenticate_user, OAuth2PasswordBearer, verify_token, OAuth2PasswordRequestForm, create_access_token
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="template")


API_KEY_NAME = "access_token"
API_KEY = os.getenv("access_token")

api_key_header = APIKeyHeader(name=API_KEY_NAME)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:58065",
    "http://127.0.0.1:51421"  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to verify API key
def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate API key")


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/initialize", dependencies=[Depends(verify_api_key)])
async def initialize_conversation():
    return JSONResponse({"message": "Conversation initialized", "thread_id": assistant_id.id})

# WebSocket handling for real-time communication
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, thread_id: str, websocket: WebSocket):
        await websocket.accept()
        if thread_id not in self.active_connections:
            self.active_connections[thread_id] = []
        self.active_connections[thread_id].append(websocket)

    def disconnect(self, thread_id: str, websocket: WebSocket):
        self.active_connections[thread_id].remove(websocket)
        if not self.active_connections[thread_id]:
            del self.active_connections[thread_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, thread_id: str):
        for connection in self.active_connections.get(thread_id, []):
            await connection.send_text(message)

manager = ConnectionManager()

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user["username"]})

    # Creating  a JSONResponse and set the cookie
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Lax")
    
    return response

def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token


@app.websocket("/ws/{thread_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str):

    

    await manager.connect(thread_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            response = await get_response(data)
            print(response)
            await manager.broadcast(response, thread_id)
    except WebSocketDisconnect:
        manager.disconnect(thread_id, websocket)
    except Exception as e:
        logger.error(f"Error: {e}")
        await websocket.close()
 


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
