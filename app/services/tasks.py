import logging
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.job import CloningJob

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="process_video_clone")
def process_video_clone(self, job_id:int, source_image_path: str, target_voice_path: str):
    """
    Entry point for the ML pipeline
    """
    db = SessionLocal()
    try:
        job = db.query(CloningJob).filter(CloningJob.id == job_id).first()
        job.status = "PROCESSING"
        db.commit()

        #TODO: Trigger F5-TTS inference
        #TODO: Trigger LivePortrait Inference

        job.status = "COMPLETED"
        job.result_url = "results/output.mp4"
        db.commit()

    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        if job:
            job.status = "FAILED"
            job.error_message = str(e)
            db.commit()
    finally:
        db.close()
