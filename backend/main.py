# main.py - апи
from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field

import mysql.connector
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column

from backend.core.config import settings

cafe_db = mysql.connector.connect(  # to do отдельный файл
    user='p',
    password='p',
    host='p',
    database='p'
)
cursor = cafe_db.cursor()

# Ещё один способ подключения бд (с сессиями)------------------------------------------------
SQLALCHEMY_DB_URL = settings.DATABASE_URL
# print("Database URL is ", SQLALCHEMY_DB_URL)
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
        yield session  # сессия открывается на время выполнения ручки в которой она вызывается


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.add_middleware(  # Прописываем каким адресам разрешено обращаться к нашему апи (из-за CORS в браузере)
    CORSMiddleware,
    allow_origins=["http://localhost:8080"]
)

coffee_menu_db = 'coffee'  # to do заменить название бд на переменную


class MenuAddSchema(BaseModel):
    name: str = Field(max_length=20)
    price: int = Field(ge=0)


class MenuSchema(MenuAddSchema):
    id: int


@app.get("/", summary="Главная страница")
def root():
    return {"Title": "Main page"}


@app.get("/menu", summary="Меню кафе (cRud)")
def menu(session: SessionDep):
    query = select(MenuModel)
    result = session.execute(query)
    return result.scalars().all()


@app.get("/menu/{item_id}", summary="Одна позиция меню")
def item(item_id: int):
    select_query = "SELECT * FROM coffee WHERE id = %s"
    cursor.execute(select_query, (item_id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail='В меню нет такой позиции')  # to do заменить коды ошибок на более подходящие


@app.post("/menu", summary="Добавление позиции (Crud)")
def add_item(item: MenuAddSchema, session: SessionDep):
    new_item = MenuModel(
        name=item.name,
        price=item.price
    )
    session.add(new_item)
    session.commit()
    return {
        "message": "Позиция успешно добавлена"
    }


@app.delete("/menu", summary="Удаление позиции (cruD)")
def delete_item(item_id: int, session: SessionDep):
    # session.delete(item_id)
    # session.commit()
    delete_query = """
        DELETE FROM coffee WHERE id = %s
        """
    cursor.execute(delete_query, (item_id,))
    cafe_db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=400, detail="Такой позиции нет")

    return {
        "message": "Позиция успешно удалена"
    }


@app.put("/menu", summary="Замена позиции (crUd)")
def replace_item(item: MenuSchema):
    replace_query = """
        UPDATE coffee SET name = %s, price = %s WHERE id = %s
    """
    values = (item.name, item.price, item.id)
    try:
        cursor.execute(replace_query, values)
        cafe_db.commit()
    except mysql.connector.errors as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Позиция заменена успешно"}


@app.patch("/menu", summary="Изменение цены позиции (crUd)")
def update_item_price(id: int, price: int):  # to do заменить на что-то такое 'id: MenuItems.id'
    update_query = """
        UPDATE coffee SET price = %s WHERE id = %s
    """
    values = (price, id)
    try:
        cursor.execute(update_query, values)
        cafe_db.commit()
    except mysql.connector.errors as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Цена обновлена успешно"}
