from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class MenuModel(Base):
    __tablename__ = "coffee"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[int]
