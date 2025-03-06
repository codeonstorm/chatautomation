from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from app.core.auth import get_current_active_user
from app.core.database import get_session
from app.models.user import User
from app.models.faq import FAQ
from app.models.chatbot import Chatbot
from app.schemas.faq import FAQCreate, FAQRead, FAQUpdate

router = APIRouter()

@router.post("", response_model=FAQRead, status_code=status.HTTP_201_CREATED)
def create_faq(
    *,
    db: Session = Depends(get_session),
    faq_in: FAQCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a frequently asked question (FAQ) entry for a chatbot
    """
    # Check if chatbot exists
    chatbot = db.get(Chatbot, faq_in.chatbot_id)
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    
    faq = FAQ(**faq_in.dict())
    
    db.add(faq)
    db.commit()
    db.refresh(faq)
    
    return faq

@router.get("", response_model=List[FAQRead])
def read_faqs(
    *,
    db: Session = Depends(get_session),
    chatbot_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve all FAQs for a chatbot
    """
    query = select(FAQ)
    
    if chatbot_id:
        query = query.where(FAQ.chatbot_id == chatbot_id)
    
    faqs = db.exec(query.offset(skip).limit(limit)).all()
    return faqs

@router.get("/{faq_id}", response_model=FAQRead)
def read_faq(
    *,
    db: Session = Depends(get_session),
    faq_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific FAQ by id
    """
    faq = db.get(FAQ, faq_id)
    
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ not found"
        )
    
    return faq

@router.put("/{faq_id}", response_model=FAQRead)
def update_faq(
    *,
    db: Session = Depends(get_session),
    faq_id: int,
    faq_in: FAQUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing FAQ
    """
    faq = db.get(FAQ, faq_id)
    
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ not found"
        )
    
    faq_data = faq_in.dict(exclude_unset=True)
    
    for key, value in faq_data.items():
        setattr(faq, key, value)
    
    faq.updated_at = datetime.utcnow()
    
    db.add(faq)
    db.commit()
    db.refresh(faq)
    
    return faq

@router.delete("/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faq(
    *,
    db: Session = Depends(get_session),
    faq_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove an FAQ entry
    """
    faq = db.get(FAQ, faq_id)
    
    if not faq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FAQ not found"
        )
    
    db.delete(faq)
    db.commit()

