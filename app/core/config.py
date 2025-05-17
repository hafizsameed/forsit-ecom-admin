import os
from typing import Optional, Dict, Any
from pydantic import BaseSettings, validator
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "E-commerce Admin Dashboard API"
    DATABASE_URL: str
    CORS_ORIGINS: list = ["*"]
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
