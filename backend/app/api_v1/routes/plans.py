from typing import Any, List
import sys

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_active_superuser, get_current_active_user
from app.core.database import get_session

from app.models.plan import Plan
from app.schemas.response import ResponseSchema
from app.schemas.plan import PlanRead

router = APIRouter(prefix="/plans", tags=["plans"])


@router.get("", response_model=list[PlanRead])
def get_plans(
    *,
    db: Session = Depends(get_session),
) -> List[PlanRead]:
    """
    Get Plans
    """
    plans = db.exec(select(Plan)).all()
    if not plans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No plans found."
        )
    return plans
