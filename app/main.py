from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.models.job import CloningJob
from app.core.config import settings
from app.api.v1.endpoints import clone



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title = settings.PROJECT_NAME,
    version = "0.1.0",
    lifespan = lifespan
)


app.include_router(clone.router, prefix=settings.API_V1_STR, tags=["cloning"])

@app.get("/health", tags=["System"])
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "Operational", "environment": "cpu-bound"}
    )