import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field, Column, JSON

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any


class FeedbackEnum(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class MessageTypeEnum(str, Enum):
    assistant = "assistant"
    user = "user"


class ChatHistory(SQLModel, table=True):
    __tablename__ = "chathistories"
    session_uuid: UUID = Field(primary_key=True)
    type: MessageTypeEnum = Field(nullable=False, description="assistant or user")
    msg: str = Field(nullable=False)
    feedback: Optional[FeedbackEnum] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    

class KnownUser(SQLModel, table=True):
    __tablename__ = "known_users"
    session_uuid: UUID = Field(primary_key=True)
    chatbot_uuid: UUID = Field(foreign_key="chatbots.uuid")
    domain_uuid: UUID = Field(foreign_key="domains.uuid")
    user_data: Optional[dict] = Field(sa_column=Column(JSON))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
