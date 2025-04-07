from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.schemas.enums import StatusEnum, VerifiedEnum, ChatbotTypeEnum, FeedbackEnum


class Plan(SQLModel, table=True):
    __tablename__ = "plans"
    id: int = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)
    description: str | None = Field(default=None)
    price: float | None = Field(nullable=False)
    billing_cycle: str | None = Field(default=None)
    status: StatusEnum = Field(default=StatusEnum.enabled)
    trial_period: int | None = Field(default=None)
    features: str = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: datetime | None = Field(default=None)
