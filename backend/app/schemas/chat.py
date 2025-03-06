from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class ChatMessageBase(BaseModel):
    role: str
    content: str

class ChatMessageCreate(ChatMessageBase):
    chat_id: int

class ChatMessageRead(ChatMessageBase):
    id: int
    uuid: str
    chat_id: int
    created_at: datetime

class ChatBase(BaseModel):
    session_id: str
    domain_id: int
    chatbot_id: int

class ChatCreate(ChatBase):
    pass

class ChatRead(ChatBase):
    id: int
    uuid: str
    created_at: datetime
    messages: List[ChatMessageRead] = []

class ChatHistoryQuery(BaseModel):
    domain_uuid: Optional[str] = None
    chatbot_uuid: Optional[str] = None
    session_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: Optional[int] = 100
    offset: Optional[int] = 0

