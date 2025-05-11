import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship, Enum as SqlEnum
from datetime import datetime
from app.schemas.enums import StatusEnum
from sqlalchemy import Column, JSON
from enum import Enum


class TaskStageEnum(str, Enum):
    in_queued = "in_queued"
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"

class TaskTypeEnum(str, Enum):
    crawl = "crawl"
    ingestion = "ingestion"

class TaskStatus(SQLModel, table=True):
    __tablename__ = "task_status"
    id: int = Field(primary_key=True)
    service_id: int = Field(nullable=False)
    type: TaskTypeEnum = Field(nullable=False)
    message_id: str = Field(nullable=True)
    meta_data: dict = Field(sa_column=Column(JSON))
    status: TaskStageEnum = Field(default=TaskStageEnum.not_started, sa_column=Column(SqlEnum(TaskStageEnum)))
    progess: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)