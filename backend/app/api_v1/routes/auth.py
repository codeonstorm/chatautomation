from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.core.config import settings
from app.core.database import get_session
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.models.user import User
from app.schemas.token import Token, RefreshToken, TokenPayload
from jose import JWTError, jwt
from pydantic import ValidationError

from app.schemas.enums import StatusEnum
from app.schemas.user import UserCreate, UserRead

from app.models.user import User
from app.models.service import Service
from app.schemas.response import ResponseSchema

from app.schemas.enums import StatusEnum
from app.core.security import get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ResponseSchema)
def register(
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
            detail="The user with this email already exists in the system",
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

    return ResponseSchema(success=True, message="User created success")


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.exec(select(User).where(User.email == form_data.username)).first()
    print(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.status == StatusEnum.disabled or user.status == StatusEnum.deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_token: RefreshToken, db: Session = Depends(get_session)
) -> Any:
    """
    Refresh token endpoint
    """
    try:
        payload = jwt.decode(
            refresh_token.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        token_data = TokenPayload(**payload)

        # Check if token is a refresh token
        if token_data.type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.exec(select(User).where(User.id == token_data.sub)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.status == StatusEnum.disabled or user.status == StatusEnum.deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/test-token", response_model=UserRead)
def test_token(current_user: UserRead = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user
