# main.py - апи
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.core.config import settings
# from backend.db.session import SessionLocal
# from backend.models import Coffee
# from backend.schemas import CoffeeResponse


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


# Dependency для получения сессии БД
# def get_db():
#     db = SessionLocal
#     try:
#         yield db
#     finally:
#         db.close()


class MenuItem(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(max_length=20)
    price: int = Field(ge=0)


items = [{
    "id": 1,
    "name": "cappuccino",
    "price": 300
}, {
    "id": 2,
    "name": "latte",
    "price": 300
}]


@app.get("/", summary="Главная страница", tags=["get эндпоинты"])
def root():
    return {
        "Title": "Main page"
    }


@app.get("/menu")
def menu():
    return items


@app.get("/menu/{item_id}")
def menu_item(item_id: int):
    for item in items:
        if item['id'] == item_id:
            return item
    raise HTTPException(status_code=404, detail='В меню нет такой позиции')


@app.post("/menu")
def add_to_menu(item: MenuItem):
    items.append(
        {
            "id": len(items) + 1,
            "name": item.name,
            "price": item.price
        }
    )
    return {"success": True}


# @app.get("/cafe", response_model=List[CoffeeResponse])
# def get_all_coffee(db: Session = Depends(get_db())):
#     coffee_list = db.query(Coffee).all()
#     return coffee_list
#
#
# print(settings.PROJECT_NAME)
