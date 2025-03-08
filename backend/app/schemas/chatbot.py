from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

class ChatbotBase(BaseModel):
    name: str
    behavior: Optional[str]
    system_prompt: str | None
    temperature: float = 0.7
    primary_color: str = "#4a56e2"
    secondary_color: str = "#ffffff"
    # domain_uuid: str
    is_active: bool = True

    @validator('temperature')
    def validate_temperature(cls, v):
        if v < 0 or v > 1:
            raise ValueError('Temperature must be between 0 and 1')
        return v

class ChatbotCreate(ChatbotBase):
    pass

class ChatbotUpdate(ChatbotBase):
    uuid: str

class ChatbotRead(ChatbotBase):
    uuid: str
    created_at: datetime
    updated_at: datetime

