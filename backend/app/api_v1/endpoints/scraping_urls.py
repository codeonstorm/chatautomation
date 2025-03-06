from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_active_user
from app.core.database import get_session
from app.models.user import User
from app.models.scraping import ScrapingURL
from app.models.domain import Domain
from app.schemas.scraping import ScrapingURLCreate, ScrapingURLRead, ScrapingURLBulkCreate

router = APIRouter()

@router.post("", response_model=List[ScrapingURLRead], status_code=status.HTTP_201_CREATED)
def create_scraping_urls(
    *,
    db: Session = Depends(get_session),
    urls_in: ScrapingURLBulkCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Add multiple URLs for web scraping
    """
    # Check if domain exists
    domain = db.get(Domain, urls_in.domain_id)
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )
    
    created_urls = []
    
    for url in urls_in.urls:
        # Check if URL already exists for this domain
        existing_url = db.exec(
            select(ScrapingURL).where(
                ScrapingURL.url == str(url),
                ScrapingURL.domain_id == urls_in.domain_id
            )
        ).first()
        
        if not existing_url:
            scraping_url = ScrapingURL(
                url=str(url),
                domain_id=urls_in.domain_id
            )
            db.add(scraping_url)
            db.commit()
            db.refresh(scraping_url)
            created_urls.append(scraping_url)
    
    return created_urls

@router.get("", response_model=List[ScrapingURLRead])
def read_scraping_urls(
    *,
    db: Session = Depends(get_session),
    domain_id: int = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all added URLs for scraping
    """
    query = select(ScrapingURL)
    
    if domain_id:
        query = query.where(ScrapingURL.domain_id == domain_id)
    
    urls = db.exec(query.offset(skip).limit(limit)).all()
    return urls

@router.delete("/{url_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scraping_url(
    *,
    db: Session = Depends(get_session),
    url_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove a specific URL from scraping list
    """
    url = db.get(ScrapingURL, url_id)
    
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    
    db.delete(url)
    db.commit()

