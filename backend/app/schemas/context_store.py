from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class ContextStore(BaseModel):
    intent: str
    context: str | None
    slots: dict[str, list[str] | None]  # slot filling entities
