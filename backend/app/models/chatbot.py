from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime
# from app.models import Domain, FAQ, Chat

class Chatbot(SQLModel, table=True):
    __tablename__ = "chatbots"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    name: str
    behavior: Optional[str] = None
    system_prompt: str
    temperature: float = Field(default=0.7)
    primary_color: str = Field(default="#4a56e2")
    secondary_color: str = Field(default="#ffffff")
    domain_id: int = Field(foreign_key="domains.id")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    domain: "Domain" = Relationship(back_populates="chatbots")
    faqs: List["FAQ"] = Relationship(back_populates="chatbot")
    chats: List["Chat"] = Relationship(back_populates="chatbot")

