import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.job import CloningJob
from app.services.tasks import process_video_clone
from app.core.config import settings


router = APIRouter()

@router.post("/clone")
async def create_cloning_job(
        source_image: UploadFile = File(...),
        target_voice: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):
    job_uuid = str(uuid.uuid4())
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    image_path = os.path.join(settings.UPLOAD_DIR, f"{job_uuid}_img_{source_image.filename}")
    voice_path = os.path.join(settings.UPLOAD_DIR, f"{job_uuid}_vox_{target_voice.filename}")

    try:
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(source_image.file, buffer)
        with open(voice_path, "wb") as buffer:
            shutil.copyfileobj(target_voice.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save error: {str(e)}")

    
    new_job = CloningJob(
        status="PENDING",
        source_image_path = image_path,
        target_audio_path = voice_path 
    )

    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)

    process_video_clone.delay(new_job.id, image_path, voice_path)

    return {"job_id": new_job.id, "status": "PENDING"}



@router.get("/download/{filename}")
async def download_video(filename: str):
    """
    Fetches the generated .mp4 file from the server's output directory.
    """
    # Security: Use os.path.basename to prevent Directory Traversal attacks (e.g., passing "../../../etc/passwd")
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(settings.OUTPUT_DIR, safe_filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404, 
            detail="Video not found. It may still be processing or the job ID is invalid."
        )
        
    return FileResponse(
        path=file_path, 
        media_type='video/mp4', 
        filename=safe_filename,
        # This header forces the browser to download the file rather than just playing it
        headers={"Content-Disposition": f"attachment; filename={safe_filename}"}
    )