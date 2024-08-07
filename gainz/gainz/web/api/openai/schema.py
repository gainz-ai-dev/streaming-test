from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class Message(BaseModel):
    role: str
    content: str


class NewThreadResponse(BaseModel):
    id: str
    object: str
    created_at: int
    metadata: Dict[str, Any]


class TextContent(BaseModel):
    value: str
    annotations: List[Any] = Field(default_factory=list)


class ContentItem(BaseModel):
    type: str
    text: TextContent


class NewMessageResponse(BaseModel):
    id: str
    object: str
    created_at: int
    assistant_id: Optional[str] = None
    thread_id: str
    run_id: Optional[str] = None
    role: str
    content: List[ContentItem] = Field(default_factory=list)
    attachments: List[Any] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ThreadMessagesListResponse(BaseModel):
    object: str
    data: List[NewMessageResponse]
    first_id: str
    last_id: str
    has_more: bool
