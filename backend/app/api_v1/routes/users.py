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

@router.post("", response_model=ResponseSchema)
def create_user(
    *,
    db: Session = Depends(get_session),
    user_in: UserCreate,
    # current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """
    Create new user
    """
    user = db.exec(select(User).where(User.email == user_in.email)).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system"
        )
    
    user_data = user_in.model_dump()
    hashed_password = get_password_hash(user_data.pop("password"))
    user = User(password=hashed_password, **user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    service = Service(user_id=user.id, plan_id=None)
    
    db.add(service)
    db.commit()
    db.refresh(service)

    return ResponseSchema(
        success=True,
        message="User created success"
    )
 