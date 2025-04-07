from typing import Any, List
import sys

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_active_superuser, get_current_active_user
from app.core.database import get_session
from app.core.security import get_password_hash
from app.schemas.user import UserCreate, UserRead

from app.models.user import User
from app.models.plan import Plan
from app.models.service import Service
from app.schemas.response import ResponseSchema

from app.schemas.enums import StatusEnum


router = APIRouter(prefix="/services", tags=["services"])


@router.get("")
def get_services(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    services: Service = session.exec(select(Service).where(Service.user_id == current_user.id)).all()

    result = []
    for i, service in enumerate(services):
      result.append({
        "id": service.id,
        "plan_id": service.plan_id,
        "status": service.status,
        "created_at": service.created_at,
        "expired_at": service.expired_at,
        "plan": session.exec(select(Plan).where(Plan.id == service.plan_id)).first()
      }) 
    
    return result


@router.get("{service_id}")
def get_service(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    service_id: int
) -> Any:
    if not current_user:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="User not found",
        )
    
    service: Service = session.exec(
      select(Service)
      .where(Service.user_id == current_user.id)
      .where(Service.id == service_id)
      ).all()

    return {
        "id": service.id,
        "plan_id": service.plan_id,
        "status": service.status,
        "created_at": service.created_at,
        "expired_at": service.expired_at,
        "plan": session.exec(select(Plan).where(Plan.id == service.plan_id)).first()
      }