from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# What user sees immediately after uploading files
class TaskResponse(BaseModel):
    task_id: str 
    status: str 
    message: str 


# What the user sees when they check the status of their video
class TaskStatusResponse(BaseModel):
    task_id: str 
    status: str 
    output_video_path: Optional[str] = None 
    created_at: datetime
