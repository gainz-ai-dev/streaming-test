import json
from typing import Dict

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from Gainz_App.db.models.users import User, current_active_user
from Gainz_App.web.api.assistants import open_ai_helper
from Gainz_App.web.api.assistants.websocket_helper import (
    ConnectionManager,
    authenticate_jwt_token,
)

router = APIRouter()
router.mount("/static", StaticFiles(directory="Gainz_App/static"), name="static")


@router.get("/start-chat")
async def initialize_conversation(
    user: User = Depends(current_active_user),
) -> Dict[str, str]:
    """
    Initialize a new OpenAI conversation thread for the current active user.

    This endpoint creates a new conversation thread and returns the unique
    identifier for the thread. It requires that the user is authenticated.

    Args:
        user (User): The currently authenticated user, obtained via dependency injection.

    Returns:
        Dict[str, str]: A dictionary containing the `thread_id` of the newly created conversation thread.

    Raises:
        HTTPException: If the user is not authenticated, a 401 Unauthorized error is raised.
    """

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    thread_id = open_ai_helper.create_thread()

    return {"thread_id": thread_id}


@router.post("/send-message/{thread_id}")
async def send_message(
    thread_id: str,
    message: str,
    user: User = Depends(current_active_user),
) -> Dict[str, str]:
    """
    Adds a message to a specific OpenAI conversation thread.

    This endpoint adds a message to the specified conversation thread and returns
    the unique identifier for the message. It requires that the user is authenticated.

    Args:
        thread_id (str): The identifier of the conversation thread to which the message will be sent.
        message (str): The message content to be added to the thread.
        user (User): The currently authenticated user, obtained via dependency injection.

    Returns:
        Dict[str, str]: A dictionary containing the `message_id` of the sent message.

    Raises:
        HTTPException: If the user is not authenticated, a 401 Unauthorized error is raised.
    """

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    message_id = open_ai_helper.add_msg_to_thread(thread_id, message)
    logger.info(f"send-message Called: {user}")

    return {"message_id": message_id}


# ------ Websocket ------
TEST_ASSISTANT_ID = "asst_1gVSgCXAiBw0s4l7pHTeWvXz"


# Instantiate the ConnectionManager
manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, thread_id: str, token: str) -> None:
    """
    Handle WebSocket connections for a given thread.

    This endpoint accepts WebSocket connections and manages communication
    based on the provided `thread_id` and `token`. It allows for real-time
    interactions over WebSocket, handling messages and events specific to
    the thread identified by `thread_id`.

    Args:
        websocket (WebSocket): The WebSocket connection object.
        thread_id (str): The identifier for the thread to which the WebSocket is connected.
        token (str): An authorization token used for validating the WebSocket connection.

    Returns:
        None: This function does not return any value. It handles WebSocket communication asynchronously.
    """

    if authenticate_jwt_token(token) is None:
        await websocket.send_text(
            "Authentication failed. Please provide a valid token.",
        )
        await websocket.close(code=4000)
        return

    await manager.connect(websocket, thread_id)

    try:
        while True:
            message = await websocket.receive_text()
            message_json = json.loads(message)

            msg_value = message_json.get("value")
            msg_type = message_json.get("msg_type")

            logger.info(f"Thread ID: {thread_id}")
            logger.info(f"Received data: {message_json}")

            if msg_type == "add_msg_to_thread":
                result = open_ai_helper.add_msg_to_thread(thread_id, msg_value)
                await manager.broadcast(
                    thread_id,
                    f"Msg: {message_json} -- Result: {result}",
                )

            elif msg_type == "run_assistant":
                event_handler = open_ai_helper.EventHandler(manager, thread_id)
                await open_ai_helper.run_assistant_on_thread(
                    TEST_ASSISTANT_ID,
                    thread_id,
                    event_handler,
                )

    except WebSocketDisconnect:
        logger.info("Client disconnected")
        await manager.disconnect(websocket, thread_id)
        await manager.broadcast(thread_id, "A user has left the chat.")

    finally:
        await manager.disconnect(websocket, thread_id)


# Should add this later to normal route instead of "/api/"
@router.get("/web_app")
def web_app() -> HTMLResponse:
    """
    Serve the HTML file for the web application.

    This endpoint serves the static HTML file located at
    `Gainz_App/static/websocket.html`.

    Returns:
        HTMLResponse: The HTML content of the web application.
    """
    return HTMLResponse(open("Gainz_App/static/websocket.html").read())


# ------ Websocket Section END------


@router.get("/hello")
def hello_endpoint() -> Dict[str, str]:
    """
    Return a simple hello message.

    This endpoint logs an informational message and returns
    a JSON response with a greeting message.

    Returns:
        Dict[str, str]: A dictionary containing the greeting message.
    """

    logger.info("Hello call received")

    return {"msg": "Hello from FastAPI"}
