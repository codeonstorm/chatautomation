from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: int = Field(primary_key=True)
    service_id: int = Field(foreign_key="services.service_id")
    email: str = Field(unique=True, index=True)
    full_name: str = Field(index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    # domains: List["Domain"] = Relationship(back_populates="user")  
    # items: List["Item"] = Relationship(back_populates="owner")

