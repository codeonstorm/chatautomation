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

from app.models.domain import Domain

from app.schemas.enums import StatusEnum
from app.schemas.domain import (
  DomainCreate,
  DomainRead,
  DomainUpdate
)
from app.schemas.user import UserRead
from app.schemas.response import ResponseSchema


router = APIRouter(prefix="/{service_id}/domains", tags=["domains"])

@router.post("", response_model=DomainRead)
def create_domain(service_id: int, domain: DomainCreate, session: Session = Depends(get_session)):
  db_domain = Domain(**domain.dict(), service_id=service_id)
  session.add(db_domain)
  session.commit()
  session.refresh(db_domain)
  return db_domain

@router.get("/{domain_id}", response_model=DomainRead)
def read_domain(service_id: int, domain_id: UUID, session: Session = Depends(get_session)):
  domain = session.exec(select(Domain).where(Domain.service_id == service_id, Domain.uuid == domain_id)).first()
  if not domain:
    raise HTTPException(status_code=404, detail="Domain not found")
  return domain

@router.get("", response_model=List[DomainRead])
def read_domains(service_id: int, session: Session = Depends(get_session)):
  return session.exec(select(Domain).where(Domain.service_id == service_id)).all()

@router.patch("/{domain_id}", response_model=DomainRead)
def update_domain(service_id: int, domain_id: UUID, domain_update: DomainUpdate, session: Session = Depends(get_session)):
  domain = session.exec(select(Domain).where(Domain.service_id == service_id, Domain.uuid == domain_id)).first()
  if not domain:
    raise HTTPException(status_code=404, detail="Domain not found")

  domain_data = domain_update.dict(exclude_unset=True)
  for key, value in domain_data.items():
    setattr(domain, key, value)

  session.add(domain)
  session.commit()
  session.refresh(domain)
  return domain

@router.delete("/{domain_id}", response_model=ResponseSchema)
def delete_domain(service_id: int, domain_id: UUID, session: Session = Depends(get_session)):
  domain = session.exec(select(Domain).where(Domain.service_id == service_id, Domain.uuid == domain_id)).first()
  if not domain:
    raise HTTPException(status_code=404, detail="Domain not found")

  session.delete(domain)
  session.commit()
  return ResponseSchema(
    success=True,
    message="Domain deleted successfully"
  )