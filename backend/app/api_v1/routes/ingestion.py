from fastapi import BackgroundTasks
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.classes.ingestion import Ingestion
from app.classes.file_helper import FileHelper
from sqlmodel import Session
from app.core.database import get_session
from pathlib import Path
import time
import sys

UPLOAD_DIR = Path("uploads")

router = APIRouter(prefix="/{service_id}/ingestion", tags=["ingestion"])

def ingest_files_embedding(service_id, chatbot_uuid, session: Session):
  ingestion = Ingestion(service_id, chatbot_uuid)
  ingestion.ingest()

# chatbot uuid,

@router.post("/{chatbot_uuid}")
async def data_ingestion(    
    service_id: int,
    chatbot_uuid: UUID,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
  ):

  # file_helper = FileHelper(UPLOAD_DIR / str(service_id))
  # files = file_helper.get_file_details()

  # print(files) 
 
  background_tasks.add_task(ingest_files_embedding, service_id, chatbot_uuid, session)
  return {"message": "success"}
