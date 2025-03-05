from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_active_user
from app.core.database import get_session
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter()

@router.get("", response_model=List[ItemRead])
def read_items(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve items
    """
    if current_user.is_superuser:
        items = db.exec(select(Item).offset(skip).limit(limit)).all()
    else:
        items = db.exec(
            select(Item)
            .where(Item.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        ).all()
    
    return items

@router.post("", response_model=ItemRead)
def create_item(
    *,
    db: Session = Depends(get_session),
    item_in: ItemCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create new item
    """
    item = Item(
        title=item_in.title,
        description=item_in.description,
        owner_id=current_user.id
    )
    
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return item

@router.get("/{item_id}", response_model=ItemRead)
def read_item(
    *,
    db: Session = Depends(get_session),
    item_id: int,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get item by ID
    """
    item = db.get(Item, item_id)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return item

@router.put("/{item_id}", response_model=ItemRead)
def update_item(
    *,
    db: Session = Depends(get_session),
    item_id: int,
    item_in: ItemUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update an item
    """
    item = db.get(Item, item_id)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    item_data = item_in.dict(exclude_unset=True)
    
    for key, value in item_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    *,
    db: Session = Depends(get_session),
    item_id: int,
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete an item
    """
    item = db.get(Item, item_id)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(item)
    db.commit()

