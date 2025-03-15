from typing import Optional
from pydantic import BaseModel, EmailStr

class PlanBase(BaseModel):
  name: str
  description: Optional[str] = None

  
class PlanBase(BaseModel):
  name: str
  description: Optional[str] = None
  price: str
  billing_cycle: str
  status: str
  trial_period: str
  features: str


class ReadPlanBase(PlanBase):
  created_at: str
  deleted_at: str



class ServiceBase(BaseModel):
  plan_id: str
  status: str
  created_at: str
  expired_at: str