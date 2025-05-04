from datetime import timedelta
from typing import Any, List
from typing import Dict, List
import json

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.core.database import get_session
from app.models.taskstatus import TaskStatus
from app.models.scrapedurls import ScrapedUrls
from tasks.tasks import start_crawl_task


router = APIRouter(prefix="/{service_id}/webscraper", tags=["webscraper"])

crawl_jobs: Dict[str, Dict] = {}
class CrawlRequest(BaseModel):
    url: str
    max_depth: int = 2
    max_pages: int = 25
    keywords: List[str] = ["rag", "openai", "crawler", "async"]
    allowed_domains: List[str] = []
    blocked_domains: List[str] = []
    patterns: List[str] = ["*guide*", "*docs*", "*tutorial*"]


@router.post("")
async def start_crawl(
    service_id: int,
    # request: CrawlRequest, 
    url: str,
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_session),
):
    job_id = start_crawl_task.send(
        service_id=service_id,
        url=url
    ) 

    tasktracker = TaskStatus(      
        service_id=service_id,
        message_id=job_id.message_id,
        meta_data=str({
            'url': url,
            'job': job_id
        })
    )
    db.add(tasktracker)
    db.commit()

    # background_tasks.add_task(run_advanced_crawler)
    # background_tasks.add_task(run_crawler_job, job_id, request)
    return {"job_id": job_id, "status": "started"}


@router.get("", response_model=List[ScrapedUrls])
async def get_urls(
    service_id: int,
    db: Session = Depends(get_session),
):
    results = db.exec(select(ScrapedUrls).where(ScrapedUrls.service_id == service_id)).all()
    if not results:
        raise HTTPException(status_code=404, detail="No URLs found")
    return results



# @router.get("/stop/{job_id}")
# async def stop_progress(job_id: str):
#     job = crawl_jobs.get(job_id)
#     if not job:
#         return {"error": "Job not found"}

#     return {
#         "status": job["status"],
#         "progress": job["progress"],
#         "total": job["total"],
#         "results_count": len(job["results"]),
#         "errors": job["errors"]
#     }


# @router.get("/progress/{job_id}")
# async def get_progress(job_id: str):
#     job = crawl_jobs.get(job_id)
#     if not job:
#         return {"error": "Job not found"}

#     return {
#         "status": job["status"],
#         "progress": job["progress"],
#         "total": job["total"],
#         "results_count": len(job["results"]),
#         "errors": job["errors"]
#     }

# @router.get("/delete/{job_id}/{index}")
# async def delete_embedding(job_id: str):
#     job = crawl_jobs.get(job_id)
#     if not job:
#         return {"error": "Job not found"}

#     return {
#         "status": job["status"],
#         "progress": job["progress"],
#         "total": job["total"],
#         "results_count": len(job["results"]),
#         "errors": job["errors"]
#     }

# @router.get("/deleteall/{job_id}")
# async def delete_embeddings(job_id: str):
#     job = crawl_jobs.get(job_id)
#     if not job:
#         return {"error": "Job not found"}

#     return {
#         "status": job["status"],
#         "progress": job["progress"],
#         "total": job["total"],
#         "results_count": len(job["results"]),
#         "errors": job["errors"]
#     }
