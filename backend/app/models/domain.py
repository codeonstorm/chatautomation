import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from app.schemas.enums import StatusEnum
# from app.models.service import Service

class Domain(SQLModel, table=True):
  __tablename__ = "domains"
  uuid: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  service_id: int = Field(foreign_key="services.id", nullable=False)    
  domain: str = Field(max_length=255, nullable=False)
  verified: bool = Field(default=False)
  status: StatusEnum = Field(default=StatusEnum.enabled)
  created_at: datetime = Field(default_factory=datetime.utcnow)