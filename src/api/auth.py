from fastapi import APIRouter, Request, Response

from src.exceptions import (
    InvalidInputException,
    InvalidInputHTTPException,
    InvalidSessionException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    WrongPasswordException,
    WrongPasswordHTTPException,
    InvalidSessionHTTPException,
)
from src.services.auth import AuthService
from src.services.user import UserService
from src.api.dependencies import DBDep, UserDep
from src.schemas.user import UserRequestAdd, UserLogin


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description="Регистрация пользователя если пользователь с таким email не зарегестрирован",
)
async def register_user(db: DBDep, user_data: UserRequestAdd):
    try:
        new_user = await AuthService(db).register_user(user_data)
    except InvalidInputException:
        raise InvalidInputHTTPException
    return {"status": "OK", "data": new_user}


@router.post(
    "/login",
    summary="Авторизация пользователя",
    description="Авторизация пользователя если пользователь существует",
)
async def login_user(db: DBDep, user_data: UserLogin, response: Response):
    try:
        access_token = await AuthService(db).login_user(user_data=user_data, response=response)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except WrongPasswordException:
        raise WrongPasswordHTTPException
    return {"status": "OK", "data": access_token}


@router.post(
    "/",
    summary="Разлогинивание пользователя",
    description="Разлогинивание пользователя путем удаления access_token(jwt)",
)
async def logout(request: Request, response: Response):
    try:
        await AuthService().logout_user(request=request, response=response)
    except InvalidSessionException:
        raise InvalidSessionHTTPException
    return {"status": "OK", "data": "Вы успешно разлогинились"}


@router.get(
    "/me",
    summary="Возвращает пользователя",
    description="Получение текущего авторизованного пользователя если авторизован",
)
async def get_me(db: DBDep, user: UserDep):
    user = await UserService(db).get_user_by_id(user_id=user.id)
    return {"status": "OK", "data": user}
