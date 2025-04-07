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


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/user")
def get_user(
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
        # Assuming service has a plan_id column that references Plan.id
        result.append({
            "id": service.id,
            "plan_id": service.plan_id,
            "status": service.status,
            "created_at": service.created_at,
            "expired_at": service.expired_at,
            "plan": session.exec(select(Plan).where(Plan.id == service.plan_id)).first()
        }) 
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "status": current_user.status,
        "last_login": current_user.last_login,
        "verified": current_user.verified,
        "created_at": current_user.created_at,
        "services": result
        # "plan": plan
    }
