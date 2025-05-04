import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from app.schemas.enums import StatusEnum
from sqlalchemy import Column, Text

class ScrapedUrls(SQLModel, table=True):
    __tablename__ = "srcaped_urls"
    id: int = Field(primary_key=True)
    service_id: int = Field(nullable=False)
    url: str = Field(sa_column=Column(Text))
    status: StatusEnum = Field(default=StatusEnum.disabled)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)