import os 
import logging
import shutil
import subprocess
from app.core.celery_app import celery_app
from app.core.database import SyncSessionLocal
from app.models.job import CloningJob
from app.core.config import settings

#ML ENGINE
from app.services.f5_tts_engine import f5_tts_engine
logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="process_video_clone")
def process_video_clone(self, job_id: int, source_image_path: str, target_voice_path: str):
    db = SyncSessionLocal()
    job = None
    try:
        job = db.get(CloningJob, job_id)
        if not job:
            return

        job.status = "PROCESSING"
        db.commit()

        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
        temp_audio = os.path.join(settings.OUTPUT_DIR, f"{job_id}_vox.wav")
        final_video_path = os.path.join(settings.OUTPUT_DIR, f"{job_id}_final.mp4")

        logger.info(f"Job {job_id}: Step 1 - Synthesizing Audio via F5-TTS...")
        target_text = "This is a stabilized, CPU-bound video cloning platform."
        f5_tts_engine.clone_voice(
            reference_audio_path=target_voice_path,
            target_text=target_text, 
            output_path=temp_audio
        )

        f5_tts_engine.unload_model() 

        logger.info(f"Job {job_id}: Sanitizing audio format for Wav2Lip...")
        clean_audio = os.path.join(settings.OUTPUT_DIR, f"{job_id}_clean_vox.wav")
        subprocess.run([
            "ffmpeg", "-y", "-i", temp_audio, 
            "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", clean_audio
        ], check=True, capture_output=True)

        logger.info(f"Job {job_id}: Step 2 - Executing Wav2Lip Lip-Sync...")
        
        vendor_script = "/app/app/vendor/Wav2Lip/inference.py"
        checkpoint_path = "/app/models/wav2lip/wav2lip_gan.pth"
        
        cmd = [
            "python", vendor_script,
            "--checkpoint_path", checkpoint_path,
            "--face", source_image_path,
            "--audio", clean_audio, 
            "--outfile", final_video_path,
            "--pads", "0", "20", "0", "0" 
        ]
        
        logger.info(f"Running Wav2Lip: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Wav2Lip Failed:\n{result.stderr}")
            raise RuntimeError("Wav2Lip inference failed.")
        
        logger.info(f"Job {job_id}: Step 3 - Pipeline Completed Successfully.")

        job.status = "COMPLETED"
        job.result_url = final_video_path
        db.commit()

    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        if job:
            job.status = "FAILED"
            job.error_message = str(e)
            db.commit()
    finally:
        db.close()
