from uuid import UUID
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.core.database import get_session

from app.models.webhook import Webhook
from app.schemas.webhook import WebhookCreate, WebhookRead
from app.schemas.response import ResponseSchema
from app.schemas.user import UserRead

router = APIRouter(prefix="/{service_id}/{chatbot_uuid}/webhook", tags=["webhooks"])

@router.post("", response_model=WebhookRead)
def create_webhook(
    service_id: int,
    chatbot_uuid: UUID,
    webhook: WebhookCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    db_webhook = Webhook(
        name=webhook.name,
        description=webhook.description,
        endpoint=webhook.endpoint,
        status=webhook.status,
        service_id=service_id, 
        chatbot_uuid=chatbot_uuid,
        basic_auth=json.dumps(webhook.basic_auth),
        header=json.dumps(webhook.header)
    )
    session.add(db_webhook)
    session.commit()
    session.refresh(db_webhook)
    return WebhookRead(
        id=db_webhook.id,
        service_id=db_webhook.service_id,
        chatbot_uuid=db_webhook.chatbot_uuid,
        name=db_webhook.name,
        description=db_webhook.description,
        endpoint=db_webhook.endpoint,
        basic_auth=json.loads(db_webhook.basic_auth) if db_webhook.basic_auth else {},
        header=json.loads(db_webhook.header) if db_webhook.header else {},
        status=db_webhook.status,
        created_at=db_webhook.created_at,
        updated_at=db_webhook.updated_at
    )

@router.get("", response_model=WebhookRead)
def read_webhook(
    service_id: int,
    chatbot_uuid: UUID,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    webhook = session.exec(
        select(Webhook).where(
            Webhook.service_id == service_id,
            Webhook.chatbot_uuid == chatbot_uuid
        )
    ).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="webhook not found")
    return WebhookRead(
        id=webhook.id,
        service_id=webhook.service_id,
        chatbot_uuid=webhook.chatbot_uuid,
        name=webhook.name,
        description=webhook.description,
        endpoint=webhook.endpoint,
        basic_auth=json.loads(webhook.basic_auth) if webhook.basic_auth else {},
        header=json.loads(webhook.header) if webhook.header else {},
        status=webhook.status,
        created_at=webhook.created_at,
        updated_at=webhook.updated_at
    )

@router.patch("", response_model=WebhookRead)
def update_webhook(
    service_id: int,
    chatbot_uuid: UUID,
    webhook_update: WebhookCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    webhook = session.exec(
        select(Webhook).where(
            Webhook.service_id == service_id,
            Webhook.chatbot_uuid == chatbot_uuid
        )
    ).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="webhook not found")

    webhook_data = webhook_update.model_dump(exclude_unset=True)
    for key, value in webhook_data.items():
        if key in {"basic_auth", "header"} and isinstance(value, dict):
            value = json.dumps(value)
        setattr(webhook, key, value)

    session.add(webhook)
    session.commit()
    session.refresh(webhook)
    return WebhookRead(
        id=webhook.id,
        service_id=webhook.service_id,
        chatbot_uuid=webhook.chatbot_uuid,
        name=webhook.name,
        description=webhook.description,
        endpoint=webhook.endpoint,
        basic_auth=json.loads(webhook.basic_auth) if webhook.basic_auth else {},
        header=json.loads(webhook.header) if webhook.header else {},
        status=webhook.status,
        created_at=webhook.created_at,
        updated_at=webhook.updated_at
    )

@router.delete("", response_model=ResponseSchema)
def delete_webhook(
    service_id: int,
    chatbot_uuid: UUID,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    webhook = session.exec(
        select(Webhook).where(
            Webhook.service_id == service_id,
            Webhook.chatbot_uuid == chatbot_uuid
        )
    ).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Function not found")

    session.delete(webhook)
    session.commit()
    return ResponseSchema(success=True, message="webhook deleted successfully")
