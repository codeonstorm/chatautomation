from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from app.core.auth import get_current_active_user
from app.core.database import get_session
from app.models.user import User
from app.models.chat import Chat, ChatMessage
from app.models.domain import Domain
from app.models.chatbot import Chatbot
from app.schemas.chat import ChatRead, ChatHistoryQuery

router = APIRouter()

@router.get("", response_model=List[ChatRead])
def read_chats(
    *,
    db: Session = Depends(get_session),
    query: ChatHistoryQuery = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """
    Fetch all chat history between clients and the chatbot
    """
    db_query = select(Chat)
    
    # Apply filters if provided
    if query.domain_uuid:
        domain = db.exec(select(Domain).where(Domain.uuid == query.domain_uuid)).first()
        if not domain:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Domain not found"
            )
        db_query = db_query.where(Chat.domain_id == domain.id)
    
    if query.chatbot_uuid:
        chatbot = db.exec(select(Chatbot).where(Chatbot.uuid == query.chatbot_uuid)).first()
        if not chatbot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chatbot not found"
            )
        db_query = db_query.where(Chat.chatbot_id == chatbot.id)
    
    if query.session_id:
        db_query = db_query.where(Chat.session_id == query.session_id)
    
    if query.start_date:
        db_query = db_query.where(Chat.created_at >= query.start_date)
    
    if query.end_date:
        db_query = db_query.where(Chat.created_at <= query.end_date)
    
    # Apply pagination
    db_query = db_query.offset(query.offset).limit(query.limit)
    
    # Execute query
    chats = db.exec(db_query).all()
    
    # Load messages for each chat
    for chat in chats:
        chat.messages = db.exec(
            select(ChatMessage)
            .where(ChatMessage.chat_id == chat.id)
            .order_by(ChatMessage.created_at)
        ).all()
    
    return chats

@router.get("/{domain_uuid}", response_model=List[ChatRead])
def read_chats_by_domain(
    *,
    db: Session = Depends(get_session),
    domain_uuid: str,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Fetch all chat history between clients and the chatbot based on domainUuid
    """
    # Find domain by UUID
    domain = db.exec(select(Domain).where(Domain.uuid == domain_uuid)).first()
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )
    
    # Get chats for this domain
    chats = db.exec(
        select(Chat)
        .where(Chat.domain_id == domain.id)
        .offset(skip)
        .limit(limit)
    ).all()
    
    # Load messages for each chat
    for chat in chats:
        chat.messages = db.exec(
            select(ChatMessage)
            .where(ChatMessage.chat_id == chat.id)
            .order_by(ChatMessage.created_at)
        ).all()
    
    return chats

