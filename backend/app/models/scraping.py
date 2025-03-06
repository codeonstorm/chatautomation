from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
import uuid
from datetime import datetime
from enum import Enum as PyEnum

class ScrapingStatus(str, PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ScrapingURL(SQLModel, table=True):
    __tablename__ = "scraping_urls"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    url: str
    title: Optional[str] = None
    domain_id: int = Field(foreign_key="domains.id")
    is_scraped: bool = Field(default=False)
    last_scraped_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    domain: "Domain" = Relationship(back_populates="urls")
    tasks: List["ScrapingTask"] = Relationship(back_populates="url")

class ScrapingTask(SQLModel, table=True):
    __tablename__ = "scraping_tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True)
    url_id: int = Field(foreign_key="scraping_urls.id")
    status: ScrapingStatus = Field(default=ScrapingStatus.PENDING)
    result: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    url: "ScrapingURL" = Relationship(back_populates="tasks")

