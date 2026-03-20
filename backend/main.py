# main.py - апи
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.db.session import get_db


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


@app.get("/menu")
def menu():
    result = get_db("SELECT * FROM coffee")
    items.clear()
    for row in result:
        items.append(
            {
                "id": len(items)+1,
                "name": row[1],
                "price": row[2]
            }
        )
    return items


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
