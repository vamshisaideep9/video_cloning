from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Video Cloning Core API"
    VERSION: str = "0.1.0"

    #Database

    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_SERVER: str 
    POSTGRES_PORT: int
    POSTGRES_DB: str 


    # Redis/Celery
    REDIS_URL: str 

    #mlflow
    DAGSHUB_MLFLOW_URI: Optional[str] = None 

    #File Paths
    UPLOAD_DIR: str 
    OUTPUT_DIR: str 

    API_V1_STR: str

    HF_TOKEN: str 
    C_FORCE_ROOT: int


    @property
    def async_database_url(self) -> str:
        encoded_pwd = quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{encoded_pwd}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property 
    def sync_database_url(self) -> str:
        encoded_pwd = quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql://{self.POSTGRES_USER}:{encoded_pwd}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()