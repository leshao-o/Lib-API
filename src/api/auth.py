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
from src.api.dependencies import DBDep, UserDep
from src.schemas.user import UserRequestAdd, UserLogin
from src.logger import logger


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description="Регистрация пользователя если пользователь с таким email не зарегестрирован",
)
async def register_user(db: DBDep, user_data: UserRequestAdd):
    logger.info("Регистрация пользователя")
    try:
        new_user = await AuthService(db).register_user(user_data)
        logger.info("Пользователь зарегистрирован успешно")
    except InvalidInputException:
        logger.error("Ошибка регистрации пользователя")
        raise InvalidInputHTTPException
    return {"status": "OK", "data": new_user}


@router.post(
    "/login",
    summary="Авторизация пользователя",
    description="Авторизация пользователя если пользователь существует",
)
async def login_user(db: DBDep, user_data: UserLogin, response: Response):
    logger.info("Авторизация пользователя")
    try:
        access_token = await AuthService(db).login_user(user_data=user_data, response=response)
        logger.info("Пользователь авторизован успешно")
    except UserNotFoundException:
        logger.error("Пользователь не найден")
        raise UserNotFoundHTTPException
    except WrongPasswordException:
        logger.error("Неправильный пароль")
        raise WrongPasswordHTTPException
    return {"status": "OK", "data": access_token}


@router.post(
    "/",
    summary="Разлогинивание пользователя",
    description="Разлогинивание пользователя путем удаления access_token(jwt)",
)
async def logout(request: Request, response: Response):
    logger.info("Разлогинивание пользователя")
    try:
        await AuthService().logout_user(request=request, response=response)
        logger.info("Пользователь разлогинен успешно")
    except InvalidSessionException:
        logger.error("Ошибка разлогинивания пользователя")
        raise InvalidSessionHTTPException
    return {"status": "OK", "data": "Вы успешно разлогинились"}


@router.get(
    "/me",
    summary="Возвращает пользователя",
    description="Получение текущего авторизованного пользователя если авторизован",
)
async def get_me(user: UserDep):
    logger.info("Получение текущего авторизованного пользователя")
    return {"status": "OK", "data": user}
