from enum import Enum
from typing import Optional, List, Any

from pydantic import BaseModel, Field


class KnowledgeBase(BaseModel):
    id: int
    name: str


class ChatRole(str, Enum):
    assistant = "assistant"
    notification_center = "notification_center"
    user = "user"


class Session(BaseModel):
    id: int
    topic: str
    title: str
    messages: Optional[List['Message']]
    latest_msg_ts: Optional[int]
    assistant_role: str
    create_at: int
    version: int


class Message:
    msg_id: int
    content: str
    text: str


class CardComponentType(str, Enum):
    text = "text"
    project_card = "project_card"
    reference = "reference"
    audio = "audio"
    expense_trace_card = "expense_trace_card"
    file = "file"
    guide_card = "guide_card"


class CardComponent(BaseModel):
    type: CardComponentType
    data: Any


class CardMessage(Message):
    title: str = ""
    components: List[CardComponent] = Field(default_factory=list)


class MessageChunkAction(int, Enum):
    append_text = 1


class ResponseChunk(BaseModel):
    action: MessageChunkAction


class AppendText(ResponseChunk):
    action: MessageChunkAction = MessageChunkAction.append_text
    text: str


class AddRef(ResponseChunk):
    sentence_id: int
    paragraph_id: int
    file_id: int
    filename: str
