from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime
# from app.models import Domain, Chatbot, Chat

class Chat(SQLModel, table=True):
    __tablename__ = "chats"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    session_id: str = Field(index=True)
    domain_id: int = Field(foreign_key="domains.id")
    chatbot_id: int = Field(foreign_key="chatbots.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    domain: "Domain" = Relationship(back_populates="chats")
    chatbot: "Chatbot" = Relationship(back_populates="chats")
    messages: List["ChatMessage"] = Relationship(back_populates="chat")

class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    chat_id: int = Field(foreign_key="chats.id")
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    chat: Chat = Relationship(back_populates="messages")

