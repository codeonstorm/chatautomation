from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime
from app.schemas.enums import ServicePlanType, ServiceStatus

class Service(SQLModel, table=True):
  
  __tablename__ = "services"
  
  service_id: int = Field(primary_key=True)
  plan: ServicePlanType = Field(default=ServicePlanType.SERVICE1)
  is_active: ServiceStatus = Field(default=ServiceStatus.ACTIVE)
  created_at: datetime = Field(default_factory=datetime.utcnow)