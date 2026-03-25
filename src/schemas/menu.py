from pydantic import BaseModel, Field


class MenuAddSchema(BaseModel):
    name: str = Field(max_length=20)
    price: int = Field(ge=0)


class MenuSchema(MenuAddSchema):
    id: int
