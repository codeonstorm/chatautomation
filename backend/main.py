import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api_v1.api import api_router
from app.chat.router import chat_router
from app.core.database import create_db_and_tables

load_dotenv()
app = FastAPI(
  title=settings.PROJECT_NAME,
  description=settings.PROJECT_DESCRIPTION,
  version=settings.VERSION,
  openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.CORS_ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)
# Include chat router directly at /chat
app.include_router(chat_router)

# @app.on_event("startup")
# def on_startup():
#   create_db_and_tables()

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

