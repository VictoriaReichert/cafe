import sqlalchemy
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import table, column, select

from backend.core.config import settings

SQLALCHEMY_DB_URL = settings.DATABASE_URL
print("Database URL is ", SQLALCHEMY_DB_URL)
# print(settings.SQL_PORT)


def get_db():
    print("Connecting...")
    try:
        engine = create_engine(SQLALCHEMY_DB_URL)

        print("We're in")
        stmt = text("SELECT * FROM coffee")
        with engine.connect() as con:
            print(con.execute(stmt).fetchall())

    except Exception as ex:
        print("Ошибка", ex)


get_db()
