"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: Optional[str] = None
    POSTGRES_USER: str = "workflow_user"
    POSTGRES_PASSWORD: str = "workflow_password"
    POSTGRES_DB: str = "workflow_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # API Keys
    OPENAI_API_KEY: str
    GEMINI_API_KEY: Optional[str] = None
    SERPAPI_API_KEY: Optional[str] = None
    
    # Application
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    # ChromaDB
    CHROMA_DB_PATH: str = "chroma_db"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

