from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API VARIABLES
    PROJECT_NAME: str = "Neural Video Cloning CPU API"
    SECRET_KEY: str 
    ALGORITHM: str 

    # DATABASE VARIABLES
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_DB: str 
    POSTGRES_HOST: str 
    POSTGRES_PORT: int 
    DATABASE_URL: str 

    # REDIS VARIABLES
    REDIS_URL: str 

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()