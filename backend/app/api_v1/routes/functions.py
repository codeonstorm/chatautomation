from datetime import timedelta
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.core.database import get_session

from app.models.user import User
from app.models.function import Function
from app.schemas.function import FunctionCreate, FunctionRead
from app.schemas.response import ResponseSchema
from app.schemas.user import UserRead

router = APIRouter(prefix="/{service_id}/functions", tags=["functions"])


@router.post("", response_model=FunctionRead)
def create_function(
    service_id: int,
    function: FunctionCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    db_function = Function(**function.model_dump(), service_id=service_id)
    session.add(db_function)
    session.commit()
    session.refresh(db_function)
    return db_function


@router.get("/{function_id}", response_model=FunctionRead)
def read_function(
    service_id: int,
    function_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    function = session.exec(
        select(Function).where(
            Function.service_id == service_id, Function.id == function_id
        )
    ).first()
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")
    return function


@router.get("", response_model=List[FunctionRead])
def read_functions(
    service_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return session.exec(select(Function).where(Function.service_id == service_id)).all()


@router.patch("/{function_id}", response_model=FunctionRead)
def update_function(
    service_id: int,
    function_id: int,
    function_update: FunctionCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    function = session.exec(
        select(Function).where(
            Function.service_id == service_id, Function.id == function_id
        )
    ).first()
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")

    function_data = function_update.dict(exclude_unset=True)
    for key, value in function_data.items():
        setattr(function, key, value)

    session.add(function)
    session.commit()
    session.refresh(function)
    return function


@router.delete("/{function_id}", response_model=ResponseSchema)
def delete_function(
    service_id: int,
    function_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    function = session.exec(
        select(Function).where(
            Function.service_id == service_id, Function.id == function_id
        )
    ).first()
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")

    session.delete(function)
    session.commit()
    return ResponseSchema(success=True, message="Function deleted successfully")
