from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.schemas.enums import StatusEnum


class Dataset(SQLModel, table=True):
    __tablename__ = "datasets"
    id: int = Field(primary_key=True)
    service_id: int = Field(foreign_key="services.id")
    name: str = Field(nullable=False)
    file_format: str | None = Field(default=None, max_length=5)
    filesize: float = Field(nullable=False)
    allowed_training: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
