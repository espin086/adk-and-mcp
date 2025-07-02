"""
Configuration settings for GPT-JobHunter Backend API
"""
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Settings
    api_title: str = "GPT-JobHunter API"
    api_description: str = "AI-Powered Job Hunting Assistant API"
    api_version: str = "1.0.0"
    debug: bool = False
    
    # Database Settings
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/jobhunter"
    database_echo: bool = False
    
    # Security Settings
    secret_key: str = "your-super-secret-jwt-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OpenAI Settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # Redis Settings (for caching and task queue)
    redis_url: str = "redis://localhost:6379/0"
    
    # External APIs
    job_search_api_key: Optional[str] = None
    linkedin_api_key: Optional[str] = None
    
    # File Upload Settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = [".pdf", ".docx", ".txt"]
    upload_folder: str = "./uploads"
    
    # CORS Settings
    cors_origins: list = ["http://localhost:8501", "http://127.0.0.1:8501"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()