from sqlalchemy import select
from fastapi import HTTPException, APIRouter
from src.api.dependencies import SessionDep
from src.models.menu import MenuModel
from src.schemas.menu import MenuSchema, MenuAddSchema
import mysql.connector

router = APIRouter()


cafe_db = mysql.connector.connect(  # to do отдельный файл УБРАТЬ
    user='root',
    password='059213369',
    host='127.0.0.1',
    database='cafe'
)
cursor = cafe_db.cursor()


@router.get("/", summary="Главная страница")
def root():
    return {"Title": "Main page"}


@router.get("/menu", summary="Меню кафе (cRud)")
def menu(session: SessionDep):
    query = select(MenuModel)
    result = session.execute(query)
    return result.scalars().all()


coffee_menu_db = 'coffee'  # to do заменить название бд на переменную


@router.get("/menu/{item_id}", summary="Одна позиция меню")
def item(item_id: int):
    select_query = "SELECT * FROM coffee WHERE id = %s"
    cursor.execute(select_query, (item_id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail='В меню нет такой позиции')  # to do заменить коды ошибок на более подходящие


@router.post("/menu", summary="Добавление позиции (Crud)")
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


@router.delete("/menu", summary="Удаление позиции (cruD)")
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


@router.put("/menu", summary="Замена позиции (crUd)")
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


@router.patch("/menu", summary="Изменение цены позиции (crUd)")
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
