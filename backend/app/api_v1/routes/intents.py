from fastapi import APIRouter, Depends
from uuid import UUID
from sqlmodel import Session

from app.core.auth import get_current_user
from app.core.database import get_session
from app.schemas.newIntent import NewIntentRead, NewIntentCreate, NewIntentUpdate
from app.schemas.response import ResponseSchema
from app.schemas.user import UserRead

from app.services.intent_service import (
    create_intent,
    get_intent,
    get_all_intents,
    update_intent,
    delete_intent,
)

router = APIRouter(prefix="/{service_id}/{chatbot_uuid}/intents", tags=["intents"])


@router.post("", response_model=NewIntentRead)
def create(
    service_id: int,
    chatbot_uuid: UUID,
    intent_in: NewIntentCreate,
    db: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return create_intent(service_id, chatbot_uuid, intent_in, db)


@router.get("/{intent_id}", response_model=NewIntentRead)
def read(
    service_id: int,
    chatbot_uuid: UUID,
    intent_id: int,
    db: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return get_intent(service_id, chatbot_uuid, intent_id, db)


@router.get("", response_model=list[NewIntentRead])
def read_all(
    service_id: int,
    chatbot_uuid: UUID,
    db: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return get_all_intents(chatbot_uuid, db)


@router.patch("/{intent_id}", response_model=NewIntentRead)
def update(
    service_id: int,
    chatbot_uuid: UUID,
    intent_id: int,
    intent_update: NewIntentUpdate,
    db: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return update_intent(service_id, chatbot_uuid, intent_id, intent_update, db)


@router.delete("/{intent_id}", response_model=ResponseSchema)
def delete(
    service_id: int,
    chatbot_uuid: UUID,
    intent_id: int,
    db: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return delete_intent(service_id, chatbot_uuid, intent_id, db)
