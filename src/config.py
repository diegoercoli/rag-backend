from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    postgres_user: str = "sigma"
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "mrwolf"
    
    # API
    api_prefix: str = "/api/v1"
    api_title: str = "RAG Experiment API"
    api_version: str = "1.0.0"
    cors_origins: List[str] = ["http://localhost:5173"]
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    class Config:
        env_file = ".env"

settings = Settings()

# ============================================================================
