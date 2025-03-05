from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_active_superuser, get_current_active_user
from app.core.database import get_session
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserRead)
def read_user_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user
    """
    return current_user

@router.put("/me", response_model=UserRead)
def update_user_me(
    *,
    db: Session = Depends(get_session),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update own user
    """
    user_data = user_in.dict(exclude_unset=True)
    
    if "password" in user_data and user_data["password"]:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    
    for key, value in user_data.items():
        setattr(current_user, key, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.get("", response_model=List[UserRead])
def read_users(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """
    Retrieve users
    """
    users = db.exec(select(User).offset(skip).limit(limit)).all()
    return users

@router.post("", response_model=UserRead)
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
    
    user_data = user_in.dict()
    hashed_password = get_password_hash(user_data.pop("password"))
    
    user = User(hashed_password=hashed_password, **user_data)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/{user_id}", response_model=UserRead)
def read_user_by_id(
    *,
    user_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get a specific user by id
    """
    user = db.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    *,
    db: Session = Depends(get_session),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """
    Update a user
    """
    user = db.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_data = user_in.dict(exclude_unset=True)
    
    if "password" in user_data and user_data["password"]:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    
    for key, value in user_data.items():
        setattr(user, key, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    *,
    db: Session = Depends(get_session),
    user_id: int,
    current_user: User = Depends(get_current_active_superuser)
) -> None:
    """
    Delete a user
    """
    user = db.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()

