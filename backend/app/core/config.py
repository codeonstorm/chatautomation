from typing import List, Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "BuyBot"
    PROJECT_DESCRIPTION: str = ""
    VERSION: str = "0.1.0"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database settings
    # DATABASE_URL: str = "sqlite:///fast"
    # DATABASE_URL: str = "mysql+mysqlconnector://root:123@localhost/fast"
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # JWT settings
    SECRET_KEY: str = "cade9c08b2bbdf09f5307df6ed02d4612892516be7f8f8447dbb662c3179660d"  # Change in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()

