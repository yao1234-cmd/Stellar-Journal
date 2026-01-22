"""
Application Configuration using Pydantic Settings
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings"""
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = "Stellar Journal"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://*.vercel.app"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:admin123@localhost:5432/stellar_journal"
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AI Provider Configuration
    AI_PROVIDER: str = "zhipu"  # 可选: "openai" 或 "zhipu"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL_EMOTION: str = "gpt-4o-mini"
    OPENAI_MODEL_WHISPER: str = "whisper-1"
    
    # 智谱 AI
    ZHIPU_API_KEY: str = ""
    ZHIPU_MODEL_EMOTION: str = "glm-4-flash"  # 或 "glm-4"
    
    # Security & Authentication
    SECRET_KEY: str = "your-secret-key-here-please-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # Email Service (Resend)
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "noreply@stellar-journal.app"
    EMAIL_FROM_NAME: str = "Stellar Journal"
    FRONTEND_URL: str = "http://localhost:3000"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_AUDIO_FORMATS: List[str] = ["mp3", "wav", "m4a", "ogg"]


settings = Settings()

