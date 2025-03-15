from pydantic import BaseModel
from datetime import datetime
from app.schemas.enums import StatusEnum
from uuid import UUID

class ChatbotBase(BaseModel):
  name: str
  description: str
  behavior: str
  system_prompt: str
  temperature: float
  primary_color: str
  secondary_color: str

class ChatbotCreate(ChatbotBase):
  name: str
  description: str

class ChatbotRead(ChatbotBase):
  uuid: UUID
  service_id: int
  created_at: datetime
  last_trained: datetime | None

class ChatbotUpdate(ChatbotBase):
  name: str | None = None
  description: str | None = None
  temperature: float | None = None
  status: StatusEnum
