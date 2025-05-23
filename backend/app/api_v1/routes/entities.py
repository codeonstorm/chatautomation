from uuid import UUID
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.core.database import get_session

from app.models.webhook import Webhook
from app.schemas.entitie import EntitiesCreate, EntitiesUpdate, EntitiesRead
from app.schemas.response import ResponseSchema
from app.schemas.user import UserRead

from app.models.entities import Entities

router = APIRouter(prefix="/{service_id}/{chatbot_uuid}/entities", tags=["entities"])

@router.post("", response_model=EntitiesRead)
def create_entity(
    service_id: int,
    chatbot_uuid: UUID,
    entity_in: EntitiesCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    entity = Entities(
        service_id=service_id,
        chatbot_uuid=chatbot_uuid,
        name=entity_in.name,
        description=entity_in.description,
        entity_type=entity_in.entity_type,
        value=json.dumps(entity_in.value)
    )
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return EntitiesRead(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        entity_type=entity.entity_type,
        value=json.loads(entity.value) if entity.value else {},
    )

@router.get("", response_model=list[EntitiesRead])
def read_entities(
    service_id: int,
    chatbot_uuid: UUID,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    entities = session.exec(
        select(Entities).where(
            Entities.service_id == service_id,
            Entities.chatbot_uuid == chatbot_uuid
        )
    ).all()

    return [
        EntitiesRead(
            id=e.id,
            name=e.name,
            description=e.description,
            entity_type=e.entity_type,
            value=json.loads(e.value) if e.value else {}
        )
        for e in entities
    ]


@router.get("/{entity_id}", response_model=EntitiesRead)
def read_entity(
    service_id: int,
    chatbot_uuid: UUID,
    entity_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    entity = session.exec(
        select(Entities).where(
            Entities.service_id == service_id,
            Entities.chatbot_uuid == chatbot_uuid,
            Entities.id == entity_id
        )
    ).first()

    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    return EntitiesRead(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        entity_type=entity.entity_type,
        value=json.loads(entity.value) if entity.value else {}
    )

@router.patch("/{entity_id}", response_model=EntitiesRead)
def update_entity(
    service_id: int,
    chatbot_uuid: UUID,
    entity_id: int,
    entity_update: EntitiesUpdate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    entity = session.exec(
        select(Entities).where(
            Entities.service_id == service_id,
            Entities.chatbot_uuid == chatbot_uuid,
            Entities.id == entity_id
        )
    ).first()

    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    entity_data = entity_update.model_dump(exclude_unset=True)
    for key, value in entity_data.items():
        if key == "value" and isinstance(value, dict):
            value = json.dumps(value)
        setattr(entity, key, value)

    session.add(entity)
    session.commit()
    session.refresh(entity)

    return EntitiesRead(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        entity_type=entity.entity_type,
        value=json.loads(entity.value) if entity.value else {}
    )


@router.delete("/{entity_id}", response_model=ResponseSchema)
def delete_entity(
    service_id: int,
    chatbot_uuid: UUID,
    entity_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    entity = session.exec(
        select(Entities).where(
            Entities.service_id == service_id,
            Entities.chatbot_uuid == chatbot_uuid,
            Entities.id == entity_id
        )
    ).first()

    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    session.delete(entity)
    session.commit()
    return ResponseSchema(success=True, message="Entity deleted successfully")
