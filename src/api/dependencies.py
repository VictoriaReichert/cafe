from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from src.database import get_session


SessionDep = Annotated[Session, Depends(get_session)]