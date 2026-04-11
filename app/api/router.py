from fastapi import APIRouter
from app.api.endpoints import video


api_router = APIRouter()

api_router.include_router(video.router, prefix="/video", tags=["Video Processing Task"])