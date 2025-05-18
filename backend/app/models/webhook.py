import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field
from datetime import datetime
from app.schemas.enums import StatusEnum
from sqlalchemy import Column, JSON
from typing import Optional, Dict



class Webhook(SQLModel, table=True):
  __tablename__ = "webhooks"
  id: int = Field(primary_key=True)
  service_id: int = Field(nullable=False)
  chatbot_uuid: UUID = Field(nullable=False)
  name: str = Field(max_length=255, nullable=False)
  description: str | None = Field(default=None)
  endpoint: str = Field(nullable=False)
  basic_auth: str | None = Field(nullable=False)
  header: Dict[str, str] | None = Field(
    sa_column=Column(JSON, nullable=True)
  )

  status: StatusEnum = Field(default=StatusEnum.enabled)
  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow)