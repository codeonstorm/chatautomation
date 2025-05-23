from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.enums import UserRoleEnum, StatusEnum
import uuid
from uuid import UUID


class ParameterBase(BaseModel):
  parameter: str
  required: bool
  message: str | None


class ActionBase(BaseModel):
  # id: int
  # intent_id: int
  name: str
  webhook: bool
  parameters: list[ParameterBase]
  

# new intent
class NewIntentBase(BaseModel):
  name: str
  description: str | None
  phrases: list[str] | None
  default_intent_responses: list[str] | None
  action: ActionBase


class NewIntentCreate(NewIntentBase):
  pass

class NewIntentUpdate(NewIntentBase):
  pass

class NewIntentRead(NewIntentBase):
  id: int
  service_id: int
  chatbot_uuid: UUID
  created_at: datetime
  updated_at: datetime
