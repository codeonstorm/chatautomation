from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime
# from app.models import Chatbot

class FAQ(SQLModel, table=True):
    __tablename__ = "faqs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    question: str
    answer: str
    chatbot_id: int = Field(foreign_key="chatbots.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    chatbot: "Chatbot" = Relationship(back_populates="faqs")

