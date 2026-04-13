from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.models.job import CloningJob



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (For production, use Alembic migrations instead)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title = "Video Cloning Core API",
    version = "0.1.0",
)


@app.get("/health", tags=["System"])
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "Operational", "environment": "cpu-bound"}
    )