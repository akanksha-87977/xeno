from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Global Transaction Validator"
    
    # Database
    # Provide safe dev defaults so running with `uvicorn` locally works
    # even when environment variables are not set.
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./app.db"
    )
    
    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-me"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3006",
        "http://localhost:3007",
        "https://frontend-five-eta-32.vercel.app",
        "https://frontend-6zqhq0xnp-akanksha-87977s-projects.vercel.app",
    ]
    
    # File Upload
    MAX_FILE_SIZE: int = 104857600  # 100MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_EXTENSIONS: List[str] = [".csv", ".xlsx", ".xls"]
    
    # Validation
    CHUNK_SIZE: int = 50000
    MAX_ROWS_PER_FILE: int = 100000
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create upload directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
