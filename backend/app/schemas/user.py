from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.enums import UserRoleEnum, StatusEnum


class UserBase(BaseModel):
    """Base model for user."""

    email: EmailStr
    name: str
    # is_active: Optional[bool] = True


class UserCreate(UserBase):
    """Model for creating a user."""

    password: str


class UserUpdate(UserBase):
    """Model for updating a user."""

    password: str


class UserRead(UserBase):
    """Model for reading user details."""

    id: int
    role: UserRoleEnum
    status: StatusEnum
    last_login: Optional[datetime] = None
    verified: bool
    created_at: datetime
