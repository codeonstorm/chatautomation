from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from app.core.auth import get_current_active_user
from app.core.database import get_session
from app.models.user import User
from app.models.chatbot import Chatbot
from app.models.domain import Domain
from app.schemas.chatbot import ChatbotCreate, ChatbotRead, ChatbotUpdate

router = APIRouter()

@router.post("", response_model=ChatbotRead, status_code=status.HTTP_201_CREATED)
def create_chatbot(
    *,
    db: Session = Depends(get_session),
    chatbot_in: ChatbotCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new chatbot
    """
    # Check if domain exists
    domain = db.get(Domain, chatbot_in.domain_id)
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )
    
    chatbot = Chatbot(**chatbot_in.dict())
    
    db.add(chatbot)
    db.commit()
    db.refresh(chatbot)
    
    return chatbot

@router.get("", response_model=List[ChatbotRead])
def read_chatbots(
    *,
    db: Session = Depends(get_session),
    domain_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all created chatbots
    """
    query = select(Chatbot)
    
    if domain_id:
        query = query.where(Chatbot.domain_id == domain_id)
    
    chatbots = db.exec(query.offset(skip).limit(limit)).all()
    return chatbots

@router.get("/{chatbot_id}", response_model=ChatbotRead)
def read_chatbot(
    *,
    db: Session = Depends(get_session),
    chatbot_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific chatbot by id
    """
    chatbot = db.get(Chatbot, chatbot_id)
    
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    
    return chatbot

@router.put("/{chatbot_id}", response_model=ChatbotRead)
def update_chatbot(
    *,
    db: Session = Depends(get_session),
    chatbot_id: int,
    chatbot_in: ChatbotUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a chatbot
    """
    chatbot = db.get(Chatbot, chatbot_id)
    
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    
    chatbot_data = chatbot_in.dict(exclude_unset=True)
    
    for key, value in chatbot_data.items():
        setattr(chatbot, key, value)
    
    chatbot.updated_at = datetime.utcnow()
    
    db.add(chatbot)
    db.commit()
    db.refresh(chatbot)
    
    return chatbot

@router.delete("/{chatbot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chatbot(
    *,
    db: Session = Depends(get_session),
    chatbot_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove a chatbot
    """
    chatbot = db.get(Chatbot, chatbot_id)
    
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    
    db.delete(chatbot)
    db.commit()

