from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_active_user
from app.core.database import get_session
from app.models.item import Item
from app.models.user import User
from app.models.domain import Domain
from app.schemas.domain import DomainAdd, DomainRead, DomainUpdate
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter()

@router.get("", response_model=List[DomainRead])
def read_domains(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve domains
    """
    if current_user.is_superuser:
        domains = db.exec(select(Domain).offset(skip).limit(limit)).all()
    else:
        domains = db.exec(
            select(Domain)
            .where(Domain.user_id == current_user.id)  # Assuming 'owner_id' links Domain to User
            .offset(skip)
            .limit(limit)
        ).all()
    
    if not domains:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    return domains

@router.post("", response_model=DomainRead)
def create_domain(
    *,
    db: Session = Depends(get_session),
    new_domain: DomainAdd,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create new item
    """
    domain = Domain(
        title=new_domain.domain,
        status=1,
        user_id=current_user.id
    )
    
    db.add(domain)
    db.commit()
    db.refresh(domain)
    
    return domain

@router.delete("/{domain}", status_code=status.HTTP_204_NO_CONTENT)
def delete_domain(
    *,
    db: Session = Depends(get_session),
    domain: str,
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete an item
    """
    row = db.exec(
          select(Domain)
          .where(Domain.domain == domain)
        ).first()
    # row = db.get(Domain, domain)
    
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    if row.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(row)
    db.commit()

