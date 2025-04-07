from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.enums import UserRoleEnum, StatusEnum


class DatasetBase(BaseModel):
    id: int
    name: str
    file_format: str | None
    filesize: float | None
    allowed_training: bool
    created_at: datetime


class DatasetUpdate(BaseModel):
    allowed_training: bool


class DatasetRead(DatasetBase):
    pass
