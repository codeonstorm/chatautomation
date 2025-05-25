from uuid import UUID
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.auth import get_current_user
from app.core.database import get_session

from app.schemas.entitie import EntitiesCreate, EntitiesUpdate, EntitiesRead
from app.schemas.response import ResponseSchema
from app.schemas.user import UserRead

from app.services.entity_service import (
    create_entity,
    read_entities,
    read_entity,
    update_entity,
    delete_entity,
)

router = APIRouter(prefix="/{service_id}/{chatbot_uuid}/entities", tags=["entities"])


@router.post("", response_model=EntitiesRead)
def create(
    service_id: int,
    chatbot_uuid: UUID,
    entity_in: EntitiesCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return create_entity(service_id, chatbot_uuid, entity_in, session)


@router.get("", response_model=list[EntitiesRead])
def read_all(
    service_id: int,
    chatbot_uuid: UUID,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return read_entities(service_id, chatbot_uuid, session)


@router.get("/{entity_id}", response_model=EntitiesRead)
def read_one(
    service_id: int,
    chatbot_uuid: UUID,
    entity_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return read_entity(service_id, chatbot_uuid, entity_id, session)


@router.patch("/{entity_id}", response_model=EntitiesRead)
def update(
    service_id: int,
    chatbot_uuid: UUID,
    entity_id: int,
    entity_update: EntitiesUpdate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return update_entity(service_id, chatbot_uuid, entity_id, entity_update, session)


@router.delete("/{entity_id}", response_model=ResponseSchema)
def delete(
    service_id: int,
    chatbot_uuid: UUID,
    entity_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return delete_entity(service_id, chatbot_uuid, entity_id, session)
