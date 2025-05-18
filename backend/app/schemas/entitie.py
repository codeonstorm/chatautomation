from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.enums import UserRoleEnum, StatusEnum
from app.models.entities import EntityTypeEnum

class BaseEntities(BaseModel):
  name: str
  description: Optional[str]
  entity_type: EntityTypeEnum
  value: dict[str, list[str]] | None

class EntitiesCreate(BaseEntities):
  pass

class EntitiesUpdate(BaseEntities):
  pass

class EntitiesRead(BaseEntities):
  id: int