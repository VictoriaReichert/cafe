# to do апи эндпоинты не должны содеражть логику, вынести в отдельный класс
from sqlalchemy import select, delete, update
from fastapi import HTTPException, APIRouter
from src.api.dependencies import SessionDep
from src.models.menu import MenuModel
from src.schemas.menu import MenuSchema, MenuAddSchema

router = APIRouter()


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
def item(item_id: int, session: SessionDep):
    query = select(MenuModel).where(MenuModel.id == item_id)
    result = session.execute(query)
    res = session.execute(query)
    if res.fetchone():  # to do доделать проверку (выбор с несуществующим id)
        return result.scalars().one()
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
    query = delete(MenuModel).where(MenuModel.id == item_id)
    result = session.execute(query)
    session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=400, detail="Такой позиции нет")
    return {
        "message": "Позиция успешно удалена"
    }


@router.put("/menu", summary="Замена позиции (crUd)")
def replace_item(item: MenuSchema, session: SessionDep):
    query = update(MenuModel).values(name=item.name, price=item.price).where(MenuModel.id == item.id)
    result = session.execute(query)
    session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=400, detail="Такой позиции нет")
    else:
        return {"message": "Позиция заменена успешно"}


@router.patch("/menu", summary="Изменение цены позиции (crUd)")
def update_item_price(id: int, new_price: int, session: SessionDep):  # to do заменить на что-то такое 'id: MenuItems.id'
    query = update(MenuModel).values(price=new_price).where(MenuModel.id == id)
    result = session.execute(query)
    session.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=400, detail="Такой позиции нет")
    else:
        return {"message": "Цена заменена успешно"}
