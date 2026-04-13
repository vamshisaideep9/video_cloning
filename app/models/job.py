import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class CloningJob(Base):
    __tablename__ = "cloning_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)

    # Storage paths
    source_image_path = Column(String, nullable=False)
    target_audio_path = Column(String, nullable=False)
    result_video_path = Column(String, nullable=True)

    # Telemetry
    mlflow_run_id = Column(String, nullable=True)
    error_logs = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

