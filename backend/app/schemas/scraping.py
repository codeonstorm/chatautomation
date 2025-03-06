from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from app.models.scraping import ScrapingStatus

class ScrapingURLBase(BaseModel):
    url: HttpUrl
    title: Optional[str] = None

class ScrapingURLCreate(ScrapingURLBase):
    domain_id: int

class ScrapingURLBulkCreate(BaseModel):
    domain_id: int
    urls: List[HttpUrl]

class ScrapingURLRead(ScrapingURLBase):
    id: int
    uuid: str
    domain_id: int
    is_scraped: bool
    last_scraped_at: Optional[datetime] = None
    created_at: datetime

class ScrapingTaskBase(BaseModel):
    url_id: int

class ScrapingTaskCreate(ScrapingTaskBase):
    pass

class ScrapingTaskRead(ScrapingTaskBase):
    id: int
    uuid: str
    status: ScrapingStatus
    result: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

class ScrapingTaskUpdate(BaseModel):
    status: Optional[ScrapingStatus] = None
    result: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class ScrapingBatchCreate(BaseModel):
    domain_id: int

