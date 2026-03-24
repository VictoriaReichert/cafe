# main.py - апи
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import mysql.connector
from backend.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

cafe_db = mysql.connector.connect(  # to do
    user='p',
    password='p',
    host='p',
    database='p'
)
cursor = cafe_db.cursor()

# Ещё один способ бд



app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.add_middleware(  # Прописываем каким адресам разрешено обращаться к нашему апи (из-за CORS)
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
def menu():
    select_query = "SELECT * FROM coffee"
    cursor.execute(select_query)
    results = cursor.fetchall()
    items = []
    for row in results:
        items.append(
            {
                "id": row[0],
                "name": row[1],
                "price": row[2]
            }
        )
    return items


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
def add_item(item: MenuAddSchema):
    insert_query = """
        INSERT INTO coffee (name, price)
        VALUES (%s, %s)
        """
    values = (item.name, item.price)
    try:
        cursor.execute(insert_query, values)
        cafe_db.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Позиция добавлена успешно"}


@app.delete("/menu", summary="Удаление позиции (cruD)")
def delete_item(item_id: int):
    delete_query = """
        DELETE FROM coffee WHERE id = %s
        """
    cursor.execute(delete_query, (item_id,))
    cafe_db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=400, detail="Такой позиции нет")

    return {"message": "Позиция удалена успешно"}


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
