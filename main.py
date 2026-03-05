# main.py - апи
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    id: int
    name: str


@app.get("/")
def root():
    return {"Hello": "World"}


items = [
    Post(id=1, name='cappuccino'),
    Post(id=2, name='latte')
]


@app.get("/menu")
async def menu() -> List[Post]:
    return items


@app.get("/menu/{id}")
async def menu_item(id: int) -> Post:
    for item in items:
        if item['id'] == id:
            return item
    raise HTTPException(status_code=404, detail='В меню нет такой позиции')


@app.get("/search")
async def search(item_id: Optional[int] = None) -> Post:
    if item_id:
        for item in items:
            if item['id'] == item_id:
                return item
    else:
        raise HTTPException(status_code=404, detail='Нет параметра для поиска')
