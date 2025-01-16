from typing import Annotated, AsyncGenerator

from fastapi import Depends, Query, Request
from pydantic import BaseModel

from src.exceptions import PermissionDeniedHTTPException, TokenDecodeException, TokenDecodeHTTPException, TokenExpireException, TokenExpireHTTPException, TokenHTTPException, UserNotFoundException, UserNotFoundHTTPException
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


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise TokenHTTPException
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().decode_token(token)
    except TokenDecodeException:
        raise TokenDecodeHTTPException
    except TokenExpireException:
        raise TokenExpireHTTPException
    return data.get("user_id")


async def get_current_user(db: DBDep, token: str = Depends(get_token)) -> User:
    try:
        user_id = get_current_user_id(token)
        user = await UserService(db).get_user_by_id(user_id=user_id)
        return user
    except UserNotFoundException:
        raise UserNotFoundHTTPException


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.is_admin:
        return current_user
    raise PermissionDeniedHTTPException


AdminUserDep = Annotated[User, Depends(get_current_admin_user)]
UserDep = Annotated[User, Depends(get_current_user)]
