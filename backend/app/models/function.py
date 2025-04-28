import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from app.schemas.enums import StatusEnum

# from app.models.service import Service


class Function(SQLModel, table=True):
    __tablename__ = "functions"
    id: int = Field(primary_key=True)
    name: str = Field(max_length=255, nullable=False)
    service_id: int = Field(nullable=False)
    intent: str | None = Field(default=None)
    description: str | None = Field(default=None)
    type: str = Field(default="api")
    endpoint_url: str = Field(nullable=False)
    require_parameters: str | None = Field(default=None)
    response_schema: str | None = Field(default=None)
    auth_type: str | None = Field(default=None)
    auth_details: str | None = Field(default=None)
    status: StatusEnum = Field(default=StatusEnum.enabled)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)