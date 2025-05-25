import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field
from datetime import datetime
from app.schemas.enums import StatusEnum
from sqlalchemy import Column, JSON
from typing import Optional, List
from sqlalchemy import Column, JSON


class Intent(SQLModel, table=True):
    __tablename__ = "intents"
    id: int = Field(primary_key=True)
    service_id: int = Field(nullable=False)
    chatbot_uuid: UUID = Field(nullable=False)
    name: str = Field(max_length=255, nullable=False)
    description: str | None = Field(default=None)
    phrases: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))
    default_intent_responses: Optional[List[str]] = Field(
        default_factory=list, sa_column=Column(JSON)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Action(SQLModel, table=True):
    __tablename__ = "actions"
    id: int = Field(primary_key=True)
    intent_id: int = Field(nullable=False)
    name: str = Field(nullable=False)
    webhook: bool = Field(default=False)


class Parameter(SQLModel, table=True):
    __tablename__ = "parameters"
    id: int = Field(primary_key=True)
    action_id: int = Field(nullable=False)
    parameter: str = Field()
    required: bool = Field(default=True)
    message: str | None = Field(default=None)
