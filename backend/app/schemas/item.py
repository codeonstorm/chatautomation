from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ItemCreate(ItemBase):
    title: str

class ItemUpdate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
    owner_id: int

