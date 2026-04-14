from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

Base = declarative_base()

# ==========================================
# ASYNC ENGINE SETUP (For FastAPI)
# ==========================================
# FIX: Use the lowercase property you defined in config.py
engine = create_async_engine(
    settings.async_database_url, 
    echo=False, 
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ==========================================
# SYNC ENGINE SETUP (For Celery Worker)
# ==========================================
# FIX: Use the lowercase property and remove the try/except block 
# so we don't accidentally hide errors anymore.

sync_engine = create_engine(
    settings.sync_database_url, 
    pool_pre_ping=True
)

SyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=sync_engine
)