from pydantic_settings import BaseSettings
from typing import List
import json
import os


class Settings(BaseSettings):
    # Application
    app_name: str = "AI Concierge Backend"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str = "sqlite:///./concierge.db"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # AI Engine
    ai_engine_enabled: bool = True
    suggestion_generation_interval_hours: int = 6
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "cors_origins":
                return json.loads(raw_val)
            return raw_val


# Create global settings instance
settings = Settings()