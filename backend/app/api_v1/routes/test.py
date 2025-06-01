from typing import Any, List
import sys

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_active_superuser, get_current_active_user
from app.core.database import get_session

from app.models.plan import Plan
from app.schemas.response import ResponseSchema
from app.schemas.plan import PlanRead

router = APIRouter(prefix="/test", tags=["test"])


@router.post("", response_model=str)
async def get_plans(
  *,
  db: Session = Depends(get_session),
):
  """
  Get Plans
  """
  return "Webhook called success!"
