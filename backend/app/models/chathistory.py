import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field, Column, JSON
from sqlalchemy.dialects.mysql import LONGTEXT

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


class KnownUser(SQLModel, table=True):
    __tablename__ = "known_users"
    uuid: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_uuid: UUID = Field(nullable=False)
    chatbot_uuid: UUID = Field(foreign_key="chatbots.uuid")
    domain_uuid: UUID = Field(foreign_key="domains.uuid")
    user_data: Optional[dict] = Field(sa_column=Column(JSON))
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatHistory(SQLModel, table=True):
    __tablename__ = "chathistories"
    id: int = Field(primary_key=True, index=True)
    chatuser: UUID = Field(foreign_key="known_users.uuid")
    type: MessageTypeEnum = Field(nullable=False, description="assistant or user")
    msg: str = Field(sa_column=Column(LONGTEXT))
    feedback: Optional[FeedbackEnum] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
