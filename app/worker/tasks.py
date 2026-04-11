from app.core.celery_app import celery
from app.core.database import SessionLocal
from app.models.video_task import VideoTask
import time
import os 


@celery.task(bind=True, name="process_video_clone")
def process_video_clone(self, task_id: str):

    db = SessionLocal()
    try:
        task = db.query(VideoTask).filter(VideoTask.task_id == task_id).first()
        if not task:
            print(f"{task_id} Error: Task not found in db.")
            return {"error": "Task not found"}
        
        task.status = "PROCESSING"
        db.commit()
        print(f"[{task_id}] status updated to processing")

        print(f"[{task_id}] Booting CPU ML Models and crunching frames...")
        time.sleep(15)


        output_path = os.path.join("/code/media", f"{task_id}_output.mp4")
        task.status = "COMPLETED"
        task.output_video_path = output_path
        db.commit()

        print(f"[{task_id}] Video cloning SUCCESSFUL!")
        return {"task_id": task_id, "status": "COMPLETED"}
    

    except Exception as e: 
        task.status = "FAILED"
        db.commit()
        print(f"[{task_id}] FAILED with error: {str(e)}")
        return {"task_id": task_id, "status": "FAILED", "error": str(e)}
    
    finally:
        db.close()


