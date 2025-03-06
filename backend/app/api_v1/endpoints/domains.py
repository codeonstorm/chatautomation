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
    domain = Domain(**domain_in.dict())
    
    db.add(domain)
    db.commit()
    db.refresh(domain)
    
    return domain

@router.get("", response_model=List[DomainRead])
def read_domains(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve domains
    """
    domains = db.exec(select(Domain).offset(skip).limit(limit)).all()
    return domains

@router.get("/{domain_id}", response_model=DomainRead)
def read_domain(
    *,
    db: Session = Depends(get_session),
    domain_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific domain by id
    """
    domain = db.get(Domain, domain_id)
    
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )
    
    return domain

@router.put("/{domain_id}", response_model=DomainRead)
def update_domain(
    *,
    db: Session = Depends(get_session),
    domain_id: int,
    domain_in: DomainUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a domain
    """
    domain = db.get(Domain, domain_id)
    
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )
    
    domain_data = domain_in.dict(exclude_unset=True)
    
    for key, value in domain_data.items():
        setattr(domain, key, value)
    
    domain.updated_at = datetime.utcnow()
    
    db.add(domain)
    db.commit()
    db.refresh(domain)
    
    return domain

@router.delete("/{domain_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_domain(
    *,
    db: Session = Depends(get_session),
    domain_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a domain
    """
    domain = db.get(Domain, domain_id)
    
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )
    
    db.delete(domain)
    db.commit()

