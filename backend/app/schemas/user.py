from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    email: EmailStr
    full_name: str
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserRead(UserBase):
    id: int

