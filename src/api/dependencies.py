from typing import Annotated, AsyncGenerator

from fastapi import Depends

from src.database import async_session_maker
from src.utils.db_manager import DBManager

# Функция для получения сессии базы данных
async def get_db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
