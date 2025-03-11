from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime
# from app.models import ScrapingURL, Chatbot, Chat
# from app.models.user import User

class Domain(SQLModel, table=True):
    __tablename__ = "domains"
    
    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    domain: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="users.id")  

