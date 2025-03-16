import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from app.schemas.enums import StatusEnum
# from app.models.service import Service

class ChatHistory(SQLModel, table=True):
  __tablename__ = "chathistories"
  chat_uuid: UUID = Field(foreign_key="chabots.uuid")
  domain_uuid: UUID = Field(foreign_key="domains.uuid")
  session_uuid: UUID = Field(foreign_key="domauns.uuid")
  # type:
  message: str = Field(nullable=False)
  feedback: str = Field(nullable=False)
  response_time: float = Field(nullable=False)
  timestamp: datetime = Field(default_factory=datetime.utcnow)


# chat_history:
#  type:enum(bot/client) | feedback:enum(positive/neutral/negative) | | timestamp | 
