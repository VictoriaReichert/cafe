import sqlalchemy
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import table, column, select

from backend.core.config import settings

SQLALCHEMY_DB_URL = settings.DATABASE_URL
# print("Database URL is ", SQLALCHEMY_DB_URL)
# print(settings.SQL_PORT)


def get_db(query: str):
    # print("Connecting...")
    try:
        engine = create_engine(SQLALCHEMY_DB_URL)

        # print("We're in")
        stmt = text(query)
        with engine.connect() as con:
            return con.execute(stmt).fetchall()

    except Exception as ex:
        print("Ошибка", ex)


res = get_db("SELECT * FROM coffee")
print(res)

