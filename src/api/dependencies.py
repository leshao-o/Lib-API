from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from src.services.user import UserService
from src.schemas.user import User
from src.services.auth import AuthService
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


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data.get("user_id")


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_current_user(db: DBDep, token: str = Depends(get_token)):
    user_id = get_current_user_id(token)
    user = await UserService(db).get_user_by_id(user_id=user_id)
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=403, detail="Недостаточно прав")


AdminUserDep = Annotated[User, Depends(get_current_admin_user)]
