from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Video Cloning Core API"
    VERSION: str = "0.1.0"

    #Database
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_SERVER: str 
    POSTGRES_DB: str 


    # Redis/Celery
    REDIS_URL: str 

    #mlflow
    DAGSHUB_MLFLOW_URI: Optional[str] = None 


    @property
    def async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    @property 
    def sync_database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()