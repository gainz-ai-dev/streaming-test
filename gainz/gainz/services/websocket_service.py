from loguru import logger
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from gainz.services.openai_client import openai_client

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        """
        Initializes a new ConnectionManager instance.
        """

        self.active_connections = {}

    async def connect(self, websocket: WebSocket, thread_id: str):
        """
        Accepts a WebSocket connection and adds it to the active connections.
        """

        await websocket.accept()
        self.active_connections[thread_id] = websocket
        logger.info(f"Connected to thread: {thread_id}")

    def disconnect(self, thread_id: str):
        """
        Removes a WebSocket connection from the active connections.
        """

        if thread_id in self.active_connections:
            del self.active_connections[thread_id]
            logger.info(f"Disconnected from thread: {thread_id}")

    async def send_message(self, message: str, thread_id: str):
        """
        Sends a message to WebSocket connection associated with the specified thread ID.
        """

        websocket = self.active_connections.get(thread_id)
        if websocket:
            await websocket.send_text(message)
            logger.info(f"Sent message to thread {thread_id}: {message}")

    async def broadcast(self, message: str):
        """
        Broadcasts a message to all active WebSocket connections.
        """

        for connection in self.active_connections.values():
            await connection.send_text(message)
            logger.info(f"Broadcast message: {message}")


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, thread_id: str = Query(None)):
    """
    WebSocket endpoint for handling real-time communication with clients.
    """

    try:
        assistant = openai_client.get_or_create_assistant()
        assistant_id = assistant.id

        if not thread_id or thread_id == "undefined":
            logger.info("No thread_id provided, creating new thread.")
            thread_response = openai_client.create_and_run_thread(
                assistant_id=assistant_id,
                messages=[
                    {"role": "user", "content": "Start the conversation."}],
                stream=True,
            )
            thread_id = None
            for event in thread_response:
                logger.info(f"event: {event}")
                if event.event == "thread.created":
                    thread_id = event.data.id
                    break
            initial_response = "Hello! How can I help you?"
        else:
            logger.info(f"Reconnecting to existing thread: {thread_id}")
            initial_response = "Reconnected to existing thread."

        await manager.connect(websocket, thread_id)
        await manager.send_message(initial_response, thread_id)

        try:
            while True:
                data = await websocket.receive_text()
                logger.info(f"Received message on thread {thread_id}")

                openai_client.add_message_to_thread(thread_id, "user", data)
                run_response = openai_client.run_assistant_on_thread(
                    thread_id, assistant_id, stream=True
                )

                cumulative_message = ""
                for event in run_response:
                    if hasattr(event, 'event') and event.event == "thread.message.delta" and event.data.delta.content:
                        cumulative_message += event.data.delta.content[0].text.value
                        await manager.send_message(cumulative_message, thread_id)
                    elif hasattr(event, 'event') and event.event == "thread.run.completed":
                        await manager.send_message('done', thread_id)
                        break

        except WebSocketDisconnect:
            manager.disconnect(thread_id)
        except Exception as e:
            logger.error(f"Error during WebSocket communication: {e}")
            await websocket.close()
    except Exception as e:
        logger.error(f"Failed to handle WebSocket connection: {e}")
        await websocket.close()
