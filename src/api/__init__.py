from fastapi import APIRouter
from src.api.cafe import router as cafe_router

main_router = APIRouter()
main_router.include_router(cafe_router)
