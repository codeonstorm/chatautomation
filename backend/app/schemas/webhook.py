from pydantic import BaseModel
from datetime import datetime
from app.schemas.enums import StatusEnum
from uuid import UUID

class WebhookBase(BaseModel):
  name: str 
  description: str | None 
  endpoint: str 
  basic_auth: dict[str, str] | None 
  header: dict[str, str] | None
  status: StatusEnum 

class WebhookCreate(WebhookBase):
  pass

class WebhookRead(WebhookBase):
  id: int 
  service_id: int 
  chatbot_uuid: UUID 
  created_at: datetime
  updated_at: datetime
