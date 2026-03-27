# to do апи эндпоинты не должны содеражть логику, вынести в отдельный класс
from sqlalchemy import select, delete, update
from fastapi import HTTPException, APIRouter
from src.api.dependencies import SessionDep
from src.models.menu import MenuModel
from src.schemas.menu import MenuSchema, MenuAddSchema
from src.logic import Logic

router = APIRouter()


@router.get("/", summary="Главная страница")
def root():
    return {"Title": "Main page"}


@router.get("/menu", summary="Меню кафе (cRud)")
def menu(session: SessionDep):
    result = Logic.select_menu(session)
    return result.scalars().all()  # to do empty menu


@router.get("/menu/{item_id}", summary="Одна позиция меню")
def item(item_id: int, session: SessionDep):
    results = Logic.select_item(item_id, session)
    if results:
        return results
    else:
        raise HTTPException(status_code=404, detail='В меню нет такой позиции')
        # to do заменить коды ошибок на более подходящие


@router.post("/menu", summary="Добавление позиции (Crud)")
def add_item(item: MenuAddSchema, session: SessionDep):
    Logic.insert_item(item, session)
    return {
        "message": "Позиция успешно добавлена"
    }


@router.delete("/menu", summary="Удаление позиции (cruD)")
def delete_item(item_id: int, session: SessionDep):
    result = Logic.delete_item(item_id, session)
    if result:
        return {
            "message": "Позиция успешно удалена"
        }
    else:
        raise HTTPException(status_code=400, detail="Такой позиции нет")


@router.put("/menu", summary="Замена позиции (crUd)")
def replace_item(item: MenuSchema, session: SessionDep):
    result = Logic.update_item(item, session)
    if result:
        return {"message": "Позиция заменена успешно"}
    else:
        raise HTTPException(status_code=400, detail="Такой позиции нет")


# @router.patch("/menu", summary="Изменение цены позиции (crUd)")
# def update_item_price(id: int, new_price: int, session: SessionDep):  # to do заменить на что-то такое 'id: MenuItems.id'
#     query = update(MenuModel).values(price=new_price).where(MenuModel.id == id)
#     result = session.execute(query)
#     session.commit()
#     if result.rowcount == 0:
#         raise HTTPException(status_code=400, detail="Такой позиции нет")
#     else:
#         return {"message": "Цена заменена успешно"}
