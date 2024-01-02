from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


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
    session: str
