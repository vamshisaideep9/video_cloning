# app/models/video_task.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class VideoTask(Base):
    __tablename__ = "video_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    status = Column(String, default="PENDING")
    source_image_path = Column(String, nullable=True)
    source_video_path = Column(String, nullable=True)
    output_video_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)