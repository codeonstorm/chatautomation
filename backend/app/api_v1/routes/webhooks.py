# routes/webhook.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.auth import get_current_user
from app.core.database import get_session
from app.schemas.user import UserRead
from app.schemas.webhook import WebhookCreate, WebhookRead
from app.schemas.response import ResponseSchema
from app.services.webhook_service import (
    create_webhook_service,
    get_webhook_service,
    update_webhook_service,
    delete_webhook_service,
)

router = APIRouter(prefix="/{service_id}/{chatbot_uuid}/webhook", tags=["webhooks"])


@router.post("", response_model=WebhookRead)
def create_webhook(
    service_id: int,
    chatbot_uuid: UUID,
    webhook: WebhookCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return create_webhook_service(service_id, chatbot_uuid, webhook, session)


@router.get("", response_model=WebhookRead)
def read_webhook(
    service_id: int,
    chatbot_uuid: UUID,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return get_webhook_service(chatbot_uuid, session)


@router.patch("", response_model=WebhookRead)
def update_webhook(
    service_id: int,
    chatbot_uuid: UUID,
    webhook_update: WebhookCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return update_webhook_service(service_id, chatbot_uuid, webhook_update, session)


@router.delete("", response_model=ResponseSchema)
def delete_webhook(
    service_id: int,
    chatbot_uuid: UUID,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return delete_webhook_service(service_id, chatbot_uuid, session)
