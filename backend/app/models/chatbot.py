import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from app.schemas.enums import StatusEnum
# from app.models.service import Service

class Chatbot(SQLModel, table=True):
  __tablename__ = "chatbots"
  uuid: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  service_id: int = Field(foreign_key="services.id", nullable=False)    
  name: str = Field(max_length=255)
  description: str = Field(max_length=255)
  behavior: str | None = Field(default=None)
  system_prompt: str | None = Field(default=None)
  temperature: float = Field(default=0.7)

  primary_color: str = Field(default="#4a56e2")
  secondary_color: str = Field(default="#ffffff")
  status: StatusEnum = Field(default=StatusEnum.enabled)
  created_at: datetime = Field(default_factory=datetime.utcnow)
  last_trained: datetime | None = Field(default=None)
  
  # traning_status |