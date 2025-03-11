from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DomainBase(BaseModel):
    domain: str

class DomainCreate(DomainBase):
    pass
    
class DomainUpdate(BaseModel):
    uuid: str 

class DomainRead(DomainBase):
    uuid: str
    is_active: bool
    created_at: datetime