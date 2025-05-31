# services/webhook_service.py
import json
from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.webhook import Webhook
from app.schemas.webhook import WebhookCreate, WebhookRead
from app.schemas.response import ResponseSchema


def create_webhook_service(service_id: int, chatbot_uuid: UUID, webhook: WebhookCreate, session: Session) -> WebhookRead:
    db_webhook = Webhook(
        name=webhook.name,
        description=webhook.description,
        endpoint=webhook.endpoint,
        status=webhook.status,
        service_id=service_id,
        chatbot_uuid=chatbot_uuid,
        basic_auth=json.dumps(webhook.basic_auth),
        header=json.dumps(webhook.header),
    )
    session.add(db_webhook)
    session.commit()
    session.refresh(db_webhook)

    return _webhook_to_read(db_webhook)


def get_webhook_service(chatbot_uuid: UUID, session: Session) -> WebhookRead:
    webhook = session.exec(
        select(Webhook).where(
            # Webhook.service_id == service_id, 
            Webhook.chatbot_uuid == chatbot_uuid
        )
    ).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="webhook not found")
    return _webhook_to_read(webhook)


def update_webhook_service(service_id: int, chatbot_uuid: UUID, webhook_update: WebhookCreate, session: Session) -> WebhookRead:
    webhook = session.exec(
        select(Webhook).where(
            Webhook.service_id == service_id, Webhook.chatbot_uuid == chatbot_uuid
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
    return _webhook_to_read(webhook)


def delete_webhook_service(service_id: int, chatbot_uuid: UUID, session: Session) -> ResponseSchema:
    webhook = session.exec(
        select(Webhook).where(
            Webhook.service_id == service_id, Webhook.chatbot_uuid == chatbot_uuid
        )
    ).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="webhook not found")

    session.delete(webhook)
    session.commit()
    return ResponseSchema(success=True, message="webhook deleted successfully")


def _webhook_to_read(webhook: Webhook) -> WebhookRead:
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
        updated_at=webhook.updated_at,
    )
