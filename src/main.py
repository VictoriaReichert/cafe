# main.py - апи
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.api import main_router


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(main_router) # матрёшка
app.add_middleware(  # Прописываем каким адресам разрешено обращаться к нашему апи (из-за CORS в браузере)
    CORSMiddleware,
    allow_origins=["http://localhost:8080"]
)

