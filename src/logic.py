from src.api.dependencies import SessionDep
from sqlalchemy import select, delete, update
from src.models.menu import MenuModel
from src.schemas.menu import MenuAddSchema, MenuSchema


class Logic:

    def select_menu(session: SessionDep):  # to do не выйдет ли так что мы открываем две сессии за раз
        query = select(MenuModel)
        result = session.execute(query)
        return result

    def select_item(item_id: int, session: SessionDep):
        query = select(MenuModel).where(MenuModel.id == item_id)
        result = session.execute(query)
        res = session.execute(query)
        if res.fetchone():  # to do доделать проверку (выбор с несуществующим id)
            return result.scalars().one()
        else:
            return None

    def insert_item(item: MenuAddSchema, session: SessionDep):
        new_item = MenuModel(
            name=item.name,
            price=item.price
        )
        session.add(new_item)
        session.commit()
        # to do в случае неудачи

    def delete_item(item_id: int, session: SessionDep):
        query = delete(MenuModel).where(MenuModel.id == item_id)
        result = session.execute(query)
        session.commit()
        if result.rowcount == 0:
            return False
        else:
            return True

    def update_item(item: MenuSchema, session: SessionDep):
        query = update(MenuModel).values(name=item.name, price=item.price).where(MenuModel.id == item.id)
        result = session.execute(query)
        session.commit()
        if result.rowcount == 0:
            return False
        else:
            return True

