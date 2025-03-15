from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.enums import UserRoleEnum, StatusEnum

class PlanBase(BaseModel):
  name: str
  description: str | None
  price: float
  billing_cycle: str | None
  status: StatusEnum
  trial_period: int | None
  features: str | None

class PlanCreate(PlanBase):
  pass

class PlanUpdate(PlanBase):
  pass

class PlanRead(PlanBase):
  id: int
  created_at: datetime
  deleted_at: datetime | None