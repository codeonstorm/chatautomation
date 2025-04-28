from pydantic import BaseModel
from datetime import datetime
from app.schemas.enums import StatusEnum
from typing import Optional

class FunctionBase(BaseModel):
  intent: str | None = None
  name: str
  description: str
  type: str = "api"
  endpoint_url: str | None = None
  require_parameters: str | None = None
  response_schema: str | None = None
  auth_type: str | None = None
  auth_details: str | None = None
  status: StatusEnum = StatusEnum.enabled

class FunctionCreate(FunctionBase):
  pass

class FunctionRead(FunctionBase):
  id: int
  created_at: datetime
  updated_at: datetime
