from enum import Enum
from typing import Optional, List, Any, Union

from pydantic import BaseModel, Field


class KnowledgeBase(BaseModel):
    id: int
    name: str


class RefFile(BaseModel):
    id: int
    origin_filename: str
    extension: str
    file_size: int
    paragraph_id_list: List[int] = []


class RefFileWithContent(RefFile):
    content: List[str] = []


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


class Message(BaseModel):
    msg_id: int = 0
    text: str
    client_ts: int


class CompleteMessage(Message):
    server_ts: int
    role: str
    is_system: bool
    is_answer: bool


class CardComponentType(str, Enum):
    text = "text"
    project_card = "project_card"
    reference = "reference"
    audio = "audio"
    expense_trace_card = "expense_trace_card"
    file = "file"
    guide_card = "guide_card"


class TextComponent(BaseModel):
    id: int
    type: CardComponentType = CardComponentType.text
    data: str


class ReferenceComponentData(BaseModel):
    pass


class RefComponent(BaseModel):
    id: int
    type: CardComponentType = CardComponentType.reference
    data: ReferenceComponentData


CardComponent = Union[TextComponent, RefComponent]


class CardMessage(BaseModel):
    components: List[CardComponent] = Field(default_factory=list)


class MessageChunkAction(int, Enum):
    base_message = 0
    append_text = 1
    AddRef = 2


class ResponseChunk(BaseModel):
    action: MessageChunkAction
    session_id: int
    msg_id: int
    data: Any

    @classmethod
    def base_message(cls, session_id: int, msg_id: int, message: CompleteMessage) -> 'ResponseChunk':
        return ResponseChunk(action=MessageChunkAction.base_message, data=message, session_id=session_id, msg_id=msg_id)

    @classmethod
    def add_text(cls, session_id: int, msg_id: int, value: str, id_: int = 0) -> 'ResponseChunk':
        return ResponseChunk(
            action=MessageChunkAction.append_text,
            data={"content": value, "id": id_},
            session_id=session_id,
            msg_id=msg_id
        )

    @classmethod
    def add_ref(cls, session_id: int, msg_id: int, ref_data: RefFile) -> 'ResponseChunk':
        if isinstance(ref_data, RefFileWithContent):
            ref_data = RefFile(**ref_data.dict())
        return ResponseChunk(action=MessageChunkAction.AddRef, data=ref_data, session_id=session_id, msg_id=msg_id)
