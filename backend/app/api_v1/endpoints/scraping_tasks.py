from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlmodel import Session, select
from datetime import datetime

from app.core.auth import get_current_active_user
from app.core.database import get_session
from app.models.user import User
from app.models.scraping import ScrapingURL, ScrapingTask, ScrapingStatus
from app.models.domain import Domain
from app.schemas.scraping import ScrapingTaskCreate, ScrapingTaskRead, ScrapingBatchCreate

router = APIRouter()

# Simulated web scraping function
async def scrape_url(db: Session, task_id: int):
    """Background task to scrape a URL"""
    task = db.get(ScrapingTask, task_id)
    if not task:
        return
    
    # Update task status to in progress
    task.status = ScrapingStatus.IN_PROGRESS
    task.started_at = datetime.utcnow()
    db.add(task)
    db.commit()
    
    try:
        # Get the URL to scrape
        url = db.get(ScrapingURL, task.url_id)
        if not url:
            task.status = ScrapingStatus.FAILED
            task.error_message = "URL not found"
            task.completed_at = datetime.utcnow()
            db.add(task)
            db.commit()
            return
        
        # Simulate scraping (in a real app, you'd use requests, BeautifulSoup, etc.)
        import asyncio
        await asyncio.sleep(5)  # Simulate work
        
        # Update task with success
        task.status = ScrapingStatus.COMPLETED
        task.result = f"Scraped content from {url.url}"
        task.completed_at = datetime.utcnow()
        
        # Update URL as scraped
        url.is_scraped = True
        url.last_scraped_at = datetime.utcnow()
        
        db.add(task)
        db.add(url)
        db.commit()
        
    except Exception as e:
        # Update task with error
        task.status = ScrapingStatus.FAILED
        task.error_message = str(e)
        task.completed_at = datetime.utcnow()
        db.add(task)
        db.commit()

@router.post("/start", response_model=List[ScrapingTaskRead], status_code=status.HTTP_201_CREATED)
async def start_scraping(
    *,
    db: Session = Depends(get_session),
    batch_in: ScrapingBatchCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user)
):
    """
    Trigger web scraping to extract data for chatbot training
    """
    # Check if domain exists
    domain = db.get(Domain, batch_in.domain_id)
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )
    
    # Get URLs for this domain that haven't been scraped yet
    urls = db.exec(
        select(ScrapingURL)
        .where(
            ScrapingURL.domain_id == batch_in.domain_id,
            ScrapingURL.is_scraped == False
        )
    ).all()
    
    if not urls:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No URLs found for scraping"
        )
    
    tasks = []
    
    # Create tasks for each URL
    for url in urls:
        task = ScrapingTask(url_id=url.id)
        db.add(task)
        db.commit()
        db.refresh(task)
        tasks.append(task)
        
        # Add scraping task to background tasks
        background_tasks.add_task(scrape_url, db, task.id)
    
    return tasks

@router.get("/status/{task_id}", response_model=ScrapingTaskRead)
def get_scraping_status(
    *,
    db: Session = Depends(get_session),
    task_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get the current status of a scraping task
    """
    task = db.get(ScrapingTask, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task

