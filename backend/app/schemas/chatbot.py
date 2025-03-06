from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

class ChatbotBase(BaseModel):
    name: str
    behavior: Optional[str] = None
    system_prompt: str
    temperature: float = 0.7
    primary_color: str = "#4a56e2"
    secondary_color: str = "#ffffff"
    domain_id: int
    is_active: bool = True

    @validator('temperature')
    def validate_temperature(cls, v):
        if v < 0 or v > 1:
            raise ValueError('Temperature must be between 0 and 1')
        return v

class ChatbotCreate(ChatbotBase):
    pass

class ChatbotUpdate(BaseModel):
    name: Optional[str] = None
    behavior: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: Optional[float] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    is_active: Optional[bool] = None

    @validator('temperature')
    def validate_temperature(cls, v):
        if v is not None and (v < 0 or v > 1):
            raise ValueError('Temperature must be between 0 and 1')
        return v

class ChatbotRead(ChatbotBase):
    id: int
    uuid: str
    created_at: datetime
    updated_at: datetime

