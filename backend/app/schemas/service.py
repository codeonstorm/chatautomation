from pydantic import BaseModel
from datetime import datetime
from app.schemas.enums import ServicePlanType, ServiceStatus

class ServiceBase(BaseModel):
  service_id: int
  plan: ServicePlanType
  is_active: ServiceStatus
  created_at: datetime

# class ServiceCreate(ServiceBase):
#   plan: ServicePlanType
#   pass

class ServiceUpdate(ServiceBase):
  plan: ServicePlanType
  plan: ServiceStatus

class ServiceStatusUpdate(ServiceBase):
  plan: ServiceStatus

class ServiceStatusUpdate(ServiceBase):
  plan: ServiceStatus