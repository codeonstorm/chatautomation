from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.schemas.enums import (
    StatusEnum,
    UserRoleEnum,
    VerifiedEnum,
    ChatbotTypeEnum,
    FeedbackEnum,
)


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(primary_key=True)
    name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password: str
    role: UserRoleEnum = Field(default=UserRoleEnum.user)
    status: StatusEnum = Field(default=StatusEnum.enabled)
    last_login: datetime | None = Field(default=None)
    verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: datetime | None = Field(default=None)


# class UserVerification(SQLModel, table=True):
#   __tablename__ = "user_verifications"
#   user_id: int = Field(foreign_key="users.id", nullable=False, ondelete="CASCADE")
#   verification_link: str = Field(max_length=255)
#   created_at: datetime = Field(default_factory=datetime.utcnow)
#   expired_at: datetime | None = Field(default=None)
