import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field
from datetime import datetime
from sqlalchemy import Column, JSON
from typing import Optional, Dict, List
from enum import Enum


class EntityTypeEnum(str, Enum):
  list = "list"
  pattern = "pattern"
  auto = "auto"


class Entities(SQLModel, table=True):
  __tablename__ = "entities"

  id: Optional[int] = Field(default=None, primary_key=True)
  service_id: int = Field(nullable=False)
  chatbot_uuid: UUID = Field(nullable=False)
  name: str = Field(max_length=255, nullable=False)
  description: Optional[str] = Field(default=None)
  entity_type: EntityTypeEnum = Field(default=EntityTypeEnum.auto)
  
  value: Optional[Dict[str, List[str]]] = Field(
    default_factory=dict,
    sa_column=Column(JSON)
  )