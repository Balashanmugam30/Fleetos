"""
Fleetos Backend Application Configuration
Module Boundary: services/api/app/config.py
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Fleetos API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # CORS Security Settings
    CORS_ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app"
    ]
    
    # Telephony Integration
    VAPI_API_KEY: str = os.getenv("VAPI_API_KEY", "")
    VAPI_PHONE_NUMBER_ID: str = os.getenv("VAPI_PHONE_NUMBER_ID", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/fleetos_db")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
