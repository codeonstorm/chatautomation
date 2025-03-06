from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime
# from app.models import ScrapingURL, Chatbot, Chat

class Domain(SQLModel, table=True):
    __tablename__ = "domains"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    name: str = Field(index=True)
    url: str
    description: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    urls: List["ScrapingURL"] = Relationship(back_populates="domain")
    chatbots: List["Chatbot"] = Relationship(back_populates="domain")
    chats: List["Chat"] = Relationship(back_populates="domain")

