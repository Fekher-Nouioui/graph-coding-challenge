"""Application configuration using Pydantic Settings."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DATABASE_URL: str #Reads from container's environment

    class Config:
        env_file = "local.env" #Fallback when starting from IDE
        case_sensitive = True


settings = Settings()
