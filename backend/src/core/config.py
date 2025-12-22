"""Application configuration settings using pydantic-settings."""
# SEMANTIC: Centralized configuration management with environment variables
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """SEMANTIC: Application settings from environment variables.
    
    All settings can be overridden via environment variables or .env file.
    """
    
    # SEMANTIC: Application metadata
    APP_NAME: str = "Web Scraping Parser API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # SEMANTIC: Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # SEMANTIC: CORS settings for frontend communication
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
    ]
    
    # SEMANTIC: Database configuration
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "parser_db"
    MONGODB_MIN_POOL_SIZE: int = 10
    MONGODB_MAX_POOL_SIZE: int = 50
    
    # SEMANTIC: Redis configuration for caching and task queue
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600  # 1 hour in seconds
    
    # SEMANTIC: Celery task queue configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_TASK_TIME_LIMIT: int = 300  # 5 minutes
    
    # SEMANTIC: HTTP client settings
    HTTP_TIMEOUT: int = 30
    HTTP_MAX_REDIRECTS: int = 10
    HTTP_RETRY_ATTEMPTS: int = 3
    
    # SEMANTIC: Parsing settings
    MAX_SITEMAP_DEPTH: int = 5
    MAX_URLS_PER_SITEMAP: int = 50000
    USER_AGENT: str = "WebParser/0.1.0 (https://github.com/madoper/parser)"
    
    # SEMANTIC: Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # SEMANTIC: Security settings
    SECRET_KEY: str = "changeme-in-production-use-long-random-string"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # SEMANTIC: Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# SEMANTIC: Create global settings instance
settings = Settings()
