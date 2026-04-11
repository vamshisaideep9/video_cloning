from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base 
from app.api.router import api_router
import app.models.video_task 


# Create all tables in the postgres database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="CPU-based asynchronous video cloning architecture"
)


app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "database": "connected"
    }