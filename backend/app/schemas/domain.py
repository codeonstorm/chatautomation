from pydantic import BaseModel
from datetime import datetime
from app.schemas.enums import StatusEnum
from uuid import UUID


class DomainBase(BaseModel):
    domain: str


class DomainCreate(DomainBase):
    pass


class DomainRead(DomainBase):
    uuid: UUID
    service_id: int
    status: StatusEnum
    created_at: datetime


class DomainUpdate(BaseModel):
    status: StatusEnum
