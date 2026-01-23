"""
Application Configuration using Pydantic Settings
"""
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import os
import json


# #region agent log
# Hypothesis A, B, D: Check raw environment variable value before Pydantic processing
env_cors = os.environ.get("BACKEND_CORS_ORIGINS", None)
print(f"[DEBUG config.py:9] Raw BACKEND_CORS_ORIGINS env var: value={repr(env_cors)}, type={type(env_cors).__name__}, len={len(env_cors) if env_cors else None}", flush=True)
# #endregion


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
    BACKEND_CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "https://*.vercel.app"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v) -> List[str]:
        # #region agent log
        # Hypothesis B, C: Check what value reaches the validator
        print(f"[DEBUG config.py:38] Validator input: value={repr(v)}, type={type(v).__name__}", flush=True)
        # #endregion
        
        # #region agent log
        # Hypothesis C: Check if empty string case
        if isinstance(v, str):
            print(f"[DEBUG config.py:44] String processing: len={len(v)}, empty={v == ''}, split_result={v.split(',') if v else []}", flush=True)
            result = [i.strip() for i in v.split(",") if i.strip()]
            print(f"[DEBUG config.py:46] String processing result: {result}", flush=True)
            return result
        # #endregion
        
        # #region agent log
        print(f"[DEBUG config.py:51] Returning value as-is: {repr(v)}", flush=True)
        # #endregion
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


# #region agent log
# Hypothesis A, D: Check if Settings instantiation succeeds
print(f"[DEBUG config.py:88] Before Settings() instantiation", flush=True)
try:
    settings = Settings()
    print(f"[DEBUG config.py:91] Settings instantiated successfully, BACKEND_CORS_ORIGINS={settings.BACKEND_CORS_ORIGINS}", flush=True)
except Exception as e:
    print(f"[DEBUG config.py:93] Settings instantiation FAILED: {type(e).__name__}: {str(e)}", flush=True)
    raise
# #endregion

