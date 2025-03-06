from typing import Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class DomainBase(BaseModel):
    name: str
    url: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

class DomainCreate(DomainBase):
    pass

class DomainUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class DomainRead(DomainBase):
    id: int
    uuid: str
    created_at: datetime
    updated_at: datetime

