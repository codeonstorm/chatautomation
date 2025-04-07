# from sqlmodel import SQLModel, Field, Relationship
# from typing import Optional
# from datetime import datetime
# from app.schemas.enums import StatusEnum, VerifiedEnum,ChatbotTypeEnum, FeedbackEnum

# # Models


# # class Service(SQLModel, table=True):
# #   __tablename__ = "services"
# #   id: Optional[int] = Field(default=None, primary_key=True)
# #   plan_id: int = Field(foreign_key="plans.id")
# #   status: StatusEnum
# #   created_at: datetime = Field(default_factory=datetime.utcnow)
# #   expired_at: Optional[datetime] = None


# # class Profile(SQLModel, table=True):
# #   __tablename__ = "profiles"
# #   user_id: int = Field(foreign_key="users.id", primary_key=True)
# #   meta_data: Optional[str] = None


# # class UserServiceSubscribed(SQLModel, table=True):
# #   __tablename__ = "user_service_subscribed"
# #   service_id: int = Field(foreign_key="services.id", primary_key=True)
# #   user_id: int = Field(foreign_key="users.id", primary_key=True)
# #   subscription_date: datetime = Field(default_factory=datetime.utcnow)
# #   status: str


# # class Domain(SQLModel, table=True):
# #   __tablename__ = "domains"
# #   id: Optional[int] = Field(default=None, primary_key=True)
# #   uuid: str
# #   service_id: int = Field(foreign_key="services.id")
# #   domain: str
# #   verified: VerifiedEnum
# #   last_checked: Optional[datetime] = None
# #   status: StatusEnum
# #   created_at: datetime = Field(default_factory=datetime.utcnow)


# # class Chatbot(SQLModel, table=True):
# #   __tablename__ = "chatbots"
# #   id: Optional[int] = Field(default=None, primary_key=True)
# #   uuid: str
# #   service_id: int = Field(foreign_key="services.id")
# #   owner_id: int = Field(foreign_key="users.id")
# #   version: str
# #   name: str
# #   description: Optional[str] = None
# #   type: ChatbotTypeEnum
# #   status: StatusEnum
# #   training_status: Optional[str] = None
# #   created_at: datetime = Field(default_factory=datetime.utcnow)
# #   last_trained: Optional[datetime] = None


# # class ChatbotData(SQLModel, table=True):
# #   __tablename__ = "chatbot_data"
# #   chatbot_id: int = Field(foreign_key="chatbots.id", primary_key=True)
# #   file_format: str
# #   data_loc: str
# #   filesize: float
# #   allowed_training: VerifiedEnum
# #   created_at: datetime = Field(default_factory=datetime.utcnow)


# # class ChatHistory(SQLModel, table=True):
# #   __tablename__ = "chat_history"
# #   chatbot_id: int = Field(foreign_key="chatbots.id", primary_key=True)
# #   domain_id: int = Field(foreign_key="domains.id")
# #   session_id: str
# #   type: str
# #   message: str
# #   feedback: FeedbackEnum
# #   response_time: Optional[float] = None
# #   timestamp: datetime = Field(default_factory=datetime.utcnow)
