# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# env_path = '.env'
env_path = 'D:\\для работы\\projects\\study\\cafe\\src\\.env'  # to do слишком длинный путь
load_dotenv(env_path)


class Settings:
    PROJECT_NAME: str = "Cafe"
    PROJECT_VERSION: str = "1.0.0"

    SQL_HOSTNAME: str = os.getenv("SQL_HOSTNAME")
    SQL_USER: str = os.getenv("SQL_USER")
    SQL_PASSWORD = os.getenv("SQL_PASSWORD")
    SQL_DB: str = os.getenv("SQL_DB")
    SQL_PORT: str = os.getenv("SQL_PORT")
    DATABASE_URL = f"mysql+pymysql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOSTNAME}:{SQL_PORT}/{SQL_DB}"
    # postgresql mysql+pymysql


settings = Settings()

# print(settings.DATABASE_URL)
