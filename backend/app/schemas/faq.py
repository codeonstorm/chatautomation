from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FAQBase(BaseModel):
    question: str
    answer: str
    chatbot_id: int

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None

class FAQRead(FAQBase):
    id: int
    uuid: str
    created_at: datetime
    updated_at: datetime

