from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Item(SQLModel, table=True):
    __tablename__ = "items"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="users.id")
    
    owner: "User" = Relationship(back_populates="items")

