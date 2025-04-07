from datetime import timedelta
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Any, List

from app.core.auth import get_current_user
from app.core.config import settings
from app.core.database import get_session

from app.models.user import User
from app.models.chatbot import Chatbot
from app.schemas.token import Token, RefreshToken, TokenPayload
from jose import JWTError, jwt

from app.schemas.enums import StatusEnum
from app.schemas.chatbot import ChatbotCreate, ChatbotUpdate, ChatbotRead
from app.schemas.user import UserRead
from app.schemas.response import ResponseSchema


router = APIRouter(prefix="/{service_id}/chatbots", tags=["chatbots"])


@router.post("", response_model=ChatbotRead)
def create_chatbot(
    service_id: int,
    chatbot: ChatbotCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    db_chatbot = Chatbot(**chatbot.model_dump(), service_id=service_id)
    session.add(db_chatbot)
    session.commit()
    session.refresh(db_chatbot)
    return db_chatbot


@router.get("/{chatbot_uuid}", response_model=ChatbotRead)
def read_chatbot(
    service_id: int,
    chatbot_uuid: UUID,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    chatbot = session.exec(
        select(Chatbot).where(
            Chatbot.service_id == service_id, Chatbot.uuid == chatbot_uuid
        )
    ).first()
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    return chatbot


@router.get("", response_model=List[ChatbotRead])
def read_chatbots(
    service_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return session.exec(select(Chatbot).where(Chatbot.service_id == service_id)).all()


@router.patch("/{chatbot_uuid}", response_model=ChatbotRead)
def update_chatbot(
    service_id: int,
    chatbot_uuid: UUID,
    chatbot_update: ChatbotUpdate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    chatbot = session.exec(
        select(Chatbot).where(
            Chatbot.service_id == service_id, Chatbot.uuid == chatbot_uuid
        )
    ).first()
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")

    chatbot_data = chatbot_update.dict(exclude_unset=True)
    for key, value in chatbot_data.items():
        setattr(chatbot, key, value)

    session.add(chatbot)
    session.commit()
    session.refresh(chatbot)
    return chatbot


@router.delete("/{chatbot_uuid}", response_model=ResponseSchema)
def delete_chatbot(
    service_id: int,
    chatbot_uuid: UUID,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    chatbot = session.exec(
        select(Chatbot).where(
            Chatbot.service_id == service_id, Chatbot.uuid == chatbot_uuid
        )
    ).first()
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")

    session.delete(chatbot)
    session.commit()
    return ResponseSchema(success=True, message="Chatbot deleted successfully")
