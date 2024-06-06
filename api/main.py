from fastapi import APIRouter

from api.routes import image_processing

api_router = APIRouter()
api_router.include_router(image_processing.router, prefix="/image_processing", tags=["users"])
