from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.chathistory import FeedbackEnum, MessageTypeEnum

class ChatHistoryBase(BaseModel):
    session_uuid: UUID
    type: MessageTypeEnum
    msg: str
    feedback: Optional[FeedbackEnum] = None

class ChatHistoryCreate(ChatHistoryBase):
    pass

class ChatHistoryRead(ChatHistoryBase):
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class KnownUserBase(BaseModel):
    session_uuid: UUID
    domain_uuid: UUID
    chatbot_uuid: UUID
    user_data: Optional[dict] = None

class KnownUserCreate(KnownUserBase):
    pass

class KnownUserRead(KnownUserBase):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
