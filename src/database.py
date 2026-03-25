# Подключение к бд (с сессиями)
from src.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


SQLALCHEMY_DB_URL = settings.DATABASE_URL
# print("Database URL is ", SQLALCHEMY_DB_URL)
engine = create_engine(SQLALCHEMY_DB_URL)

new_session = sessionmaker(engine, expire_on_commit=False)


def get_session():
    with new_session() as session:
        yield session  # сессия открывается на время выполнения ручки в которой она вызывается


class Base(DeclarativeBase):
    pass
