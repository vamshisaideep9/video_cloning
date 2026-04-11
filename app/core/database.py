# app/core/database.py

"""
Using SQLAlchemy to connect to postgres 

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings


# Create the SQLAlchemy engine using the secure URL
engine = create_engine(settings.DATABASE_URL, echo=False)

# SessionLocal will be used to spawn database sessions for each API request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All your future database models will inherit from this Base
Base = declarative_base()



# Dependency injection function for FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()