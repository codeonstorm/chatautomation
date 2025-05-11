from fastapi import BackgroundTasks
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.classes.ingestion import Ingestion
from app.classes.file_helper import FileHelper
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.taskstatus import TaskStatus, TaskStageEnum, TaskTypeEnum
from pathlib import Path
import time
import sys

UPLOAD_DIR = Path("uploads")

router = APIRouter(prefix="/{service_id}/ingestion", tags=["ingestion"])

def ingest_files_embedding(taskid, service_id, chatbot_uuid):
  ingestion = Ingestion(taskid, service_id, chatbot_uuid)
  ingestion.ingest()

# chatbot uuid,

@router.post("/{chatbot_uuid}")
async def data_ingestion(    
    service_id: int,
    chatbot_uuid: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_session),
  ):

  # file_helper = FileHelper(UPLOAD_DIR / str(service_id))
  # files = file_helper.get_file_details()

  # print(files) 
  tasktracker = TaskStatus(      
      service_id=service_id,
      type=TaskTypeEnum.ingestion,
      message_id='',
      meta_data='',
      status=TaskStageEnum.in_queued,
  )
  db.add(tasktracker)
  db.commit()
  db.refresh(tasktracker)
  print(tasktracker.id)
  background_tasks.add_task(ingest_files_embedding, tasktracker.id, service_id, chatbot_uuid)

  return {"message": "success"}


@router.get("/progress", response_model=list[TaskStatus])
async def get_progress(
    service_id: int,
    db: Session = Depends(get_session),
):
    results = db.exec(
      select(TaskStatus)
      .where(TaskStatus.service_id == service_id)
      .where(TaskStatus.type == TaskTypeEnum.ingestion)
      .order_by(TaskStatus.created_at.desc())
    ).all()
    if not results:
        return []
    return results
