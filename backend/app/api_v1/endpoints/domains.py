from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_active_user
from app.core.database import get_session
from app.models.user import User
from app.models.domain import Domain
from app.schemas.domain import DomainCreate, DomainRead, DomainUpdate

router = APIRouter()

@router.post("", response_model=DomainRead, status_code=status.HTTP_201_CREATED)
def create_domain(
    *,
    db: Session = Depends(get_session),
    domain_in: DomainCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new domain for chatbot
    """
    domain = Domain(
        domain=domain_in.domain,
        is_active=True,
        user_id=current_user.id
    )
    
    db.add(domain)
    db.commit()
    db.refresh(domain)
    
    return domain

@router.get("", response_model=List[DomainRead], status_code=status.HTTP_200_OK)
def read_domains(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    domains = db.exec(select(Domain).where(Domain.user_id == current_user.id).offset(skip).limit(limit)).all()
    return domains

@router.get("/{uuid}", response_model=DomainRead)
def read_domain(
    *,
    db: Session = Depends(get_session),
    uuid: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific domain by uuid
    """
    # domain = db.get(Domain, domain_id)
    domain = db.exec(
        select(Domain)
        .where(Domain.user_id == current_user.id)
        .where(Domain.uuid == uuid)
    ).first()
    
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )
    
    return domain

@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_domain(
    *,
    db: Session = Depends(get_session),
    uuid: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a domain
    """
    domain = db.exec(
        select(Domain)
        .where(Domain.user_id == current_user.id)
        .where(Domain.uuid == uuid)
    ).first()
    
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )
    
    db.delete(domain)
    db.commit()

