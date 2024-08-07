from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from loguru import logger

from gainz.web.api.openai.schema import (
    Message, NewThreadResponse, NewMessageResponse,
)
from gainz.services.openai_client import openai_client

router = APIRouter()


@router.post("/threads/", response_model=NewThreadResponse)
def create_new_thread():
    """
    Initialize a new conversation by creating a new thread.
    """
    try:
        thread = openai_client.create_thread()
        return thread
    except Exception as e:
        logger.error(f"Error initializing new thread: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to create a new thread")


@router.post("/threads/{thread_id}/messages/", response_model=NewMessageResponse)
def send_message_to_thread(thread_id: str, message: Message):
    """
    Send a message to an existing thread.
    """
    try:
        response = openai_client.add_message_to_thread(
            thread_id, message.role, message.content
        )
        return response
    except Exception as e:
        logger.error(f"Error sending message to thread {thread_id}: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to send message to the thread")


@router.get("/threads/{thread_id}/messages/")
def list_messages_from_thread(thread_id: str, limit: int = 20, order: str = 'desc'):
    """
    List messages from a given thread.
    """
    try:
        messages = openai_client.list_thread_messages(
            thread_id, limit=limit, order=order)
        return messages
    except Exception as e:
        logger.error(f"Error listing messages for thread {thread_id}: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to list messages for the thread")
