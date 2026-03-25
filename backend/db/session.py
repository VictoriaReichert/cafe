import sqlalchemy
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column

from backend.core.config import settings

SQLALCHEMY_DB_URL = settings.DATABASE_URL
# print("Database URL is ", SQLALCHEMY_DB_URL)
# print(settings.SQL_PORT)


engine = create_engine(SQLALCHEMY_DB_URL)

new_session = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class MenuModel(Base):
    __tablename__ = "coffee"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[int]


def get_session():
    with new_session() as session:
        yield session


def execute_db_query(query: str):
    # print("Connecting...")
    try:
        engine = create_engine(SQLALCHEMY_DB_URL)

        # print("We're in")
        stmt = text(query)
        items = []
        with engine.connect() as con:
            for row in con.execute(stmt).fetchall():
                items.append(
                    {
                        "id": len(items) + 1,
                        "name": row[1],
                        "price": row[2]
                    }
                )
            engine.dispose()
            return items  # as json
    except Exception as ex:
        print("Ошибка", ex)


res = execute_db_query("SELECT * FROM coffee")
print(res)

# Ошибка 'cryptography' package is required for sha256_password or caching_sha2_password auth methods
