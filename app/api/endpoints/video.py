


from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import uuid
import os
import shutil


from app.core.database import get_db 
from app.models.video_task import VideoTask
from app.schemas.video_task import TaskResponse, TaskStatusResponse
from app.worker.tasks import process_video_clone

router = APIRouter()

MEDIA_DIR = "/code/media"
os.makedirs(MEDIA_DIR, exist_ok=True)

@router.post("/clone", response_model=TaskResponse)
async def create_clone_task(
    source_image: UploadFile = File(..., description="The static face to animate"),
    driving_video: UploadFile = File(..., description="The video containing the motion/audio"),
    db: Session = Depends(get_db)
):
    task_id = str(uuid.uuid4())

    image_path = os.path.join(MEDIA_DIR, f"{task_id}_{source_image.filename}")
    video_path = os.path.join(MEDIA_DIR, f"{task_id}_{driving_video.filename}")

    try:
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(source_image.file, buffer)
        
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(driving_video.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save files: {str(e)}")
    
    
    
    new_task = VideoTask(
        task_id=task_id,
        status="PENDING",
        source_image_path=image_path,
        source_video_path=video_path
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)


    process_video_clone.delay(task_id)

    return {
        "task_id": task_id,
        "status": "PENDING",
        "message": "Files uploaded successfully. Task is queued."
    }


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str, db: Session = Depends(get_db)):
    task = db.query(VideoTask).filter(VideoTask.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return task