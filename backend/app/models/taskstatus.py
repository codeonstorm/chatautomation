import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from app.schemas.enums import StatusEnum
from sqlalchemy import Column, JSON

class TaskStatus(SQLModel, table=True):
    __tablename__ = "task_status"
    id: int = Field(primary_key=True)
    service_id: int = Field(nullable=False)
    message_id: str = Field(nullable=True)
    meta_data: dict = Field(sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)