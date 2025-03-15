from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.schemas.enums import StatusEnum, UserRoleEnum, VerifiedEnum,ChatbotTypeEnum, FeedbackEnum

class Service(SQLModel, table=True):
  __tablename__ = "services"
  id: int = Field(primary_key=True)
  user_id: int = Field(foreign_key='users.id', nullable=False, ondelete='CASCADE')
  plan_id: int | None = Field(foreign_key='plans.id', ondelete="SET NULL", nullable=True)
  status: StatusEnum = Field(default=StatusEnum.enabled)
  created_at: datetime = Field(default_factory=datetime.utcnow)
  expired_at: datetime | None = Field(default=None)