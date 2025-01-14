from typing import Annotated, AsyncGenerator

from fastapi import Depends, Query
from pydantic import BaseModel

from src.database import async_session_maker
from src.utils.db_manager import DBManager

# Функция для получения сессии базы данных
async def get_db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


# Модель для пагинации, которая будет использоваться в запросах
class Pagination(BaseModel):
    page: Annotated[int, Query(default=1, ge=1)]
    per_page: Annotated[int, Query(default=5, ge=1, lt=20)]


PaginationDep = Annotated[Pagination, Depends()]
