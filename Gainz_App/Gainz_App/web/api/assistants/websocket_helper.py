from typing import Dict, List, Optional

from fastapi import WebSocket
from jose import JWTError
from jwt import ExpiredSignatureError, decode
from loguru import logger

from Gainz_App.settings import settings

# Globals
SECRET_KEY = settings.users_secret
ALGORITHM = settings.jwt_algorithm
EXPECTED_AUDIENCE = "fastapi-users:auth"


class ConnectionManager:
    def __init__(self) -> None:
        """
        Initialize the ConnectionManager with an empty dictionary to store WebSocket connections.

        The connections are stored in a dictionary where the key is a thread_id and the value
        is a list of WebSocket connections associated with that thread_id.
        """

        # Store connections by thread_id
        self.connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, thread_id: str) -> None:
        """
        Accept a WebSocket connection and add it to the connections dictionary.

        If the thread_id is not already present in the dictionary, it initializes an empty list for it.

        Args:
            websocket (WebSocket): The WebSocket connection object to be added.
            thread_id (str): The identifier for the thread to which the WebSocket is connected.

        Returns:
            None: This method does not return a value.
        """

        await websocket.accept()
        if thread_id not in self.connections:
            self.connections[thread_id] = []
        self.connections[thread_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, thread_id: str) -> None:
        """
        Remove a WebSocket connection from the connections dictionary.

        If the thread_id is present, it attempts to remove the WebSocket. If the list for that thread_id
        becomes empty, it deletes the entry for that thread_id. If the WebSocket is not found, it logs a warning.

        Args:
            websocket (WebSocket): The WebSocket connection object to be removed.
            thread_id (str): The identifier for the thread from which the WebSocket is to be removed.

        Returns:
            None: This method does not return a value.
        """

        if thread_id in self.connections:
            try:
                self.connections[thread_id].remove(websocket)
                if not self.connections[thread_id]:
                    del self.connections[thread_id]
            except ValueError:
                logger.warning(
                    f"WebSocket not found in thread_id {thread_id} connections",
                )
        else:
            logger.warning(f"Thread ID {thread_id} not found in connections")

    async def broadcast(self, thread_id: str, message: str) -> None:
        """
        Send a message to all WebSocket connections associated with a specific thread_id.

        This method iterates over all WebSocket connections for the given thread_id and attempts
        to send the message to each one. If an error occurs during sending, it logs the error and
        disconnects the WebSocket.

        Args:
            thread_id (str): The identifier for the thread to which the message will be broadcasted.
            message (str): The message to be sent to all WebSocket connections.

        Returns:
            None: This method does not return a value.
        """

        if thread_id in self.connections:
            connections = self.connections[thread_id].copy()
            for connection in connections:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending message: {e}")
                    await self.disconnect(connection, thread_id)


def authenticate_jwt_token(token: str) -> Optional[str]:
    """
    Authenticate a JWT token and return the user ID if valid.

    This function decodes and validates the provided JWT token. It checks
    for expiration and other JWT errors. If the token is valid and contains
    a user ID, the function returns the user ID. Otherwise, it returns None.

    Args:
        token (str): The JWT token to be authenticated.

    Returns:
        Optional[str]: The user ID extracted from the token if valid, otherwise None.

    Raises:
        Exception: Logs errors related to token expiration, JWT issues, or unexpected errors.
    """

    try:
        payload = decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=EXPECTED_AUDIENCE,
        )

        logger.info(f"Payload: {payload}")
        user_id = payload.get("sub")

        if user_id is None:
            logger.error("User not authenticated")
            return None

        return user_id

    except ExpiredSignatureError:
        logger.error("Token has expired")
        return None

    except JWTError as e:
        logger.error(f"JWT error: {e!s}")
        return None

    except Exception as e:
        logger.error(f"Unexpected error: {e!s}")
        return None
