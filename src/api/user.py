from fastapi import APIRouter

from src.exceptions import (
    InvalidInputException,
    InvalidInputHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
)
from src.schemas.user import UserPatch
from src.services.user import UserService
from src.api.dependencies import DBDep, AdminUserDep, PaginationDep, UserDep
from src.logger import logger


router = APIRouter(prefix="/user", tags=["Пользователи"])


@router.get(
    "/",
    summary="Возвращает список пользователей",
    description="Получение списка всех пользователей. Только для админов",
)
async def get_all_users(admin_user: AdminUserDep, db: DBDep, pagination: PaginationDep):
    logger.info("Получение списка пользователей")
    try:
        users = await UserService(db).get_all_users()
    except UserNotFoundException:
        logger.error("Пользователи не найдены")
        raise UserNotFoundHTTPException
    users = users[pagination.per_page * (pagination.page - 1) :][: pagination.per_page]
    logger.info(f"Список пользователей получен успешно. Количество пользователей: {len(users)}")
    return {"status": "OK", "data": users}


@router.put(
    "/{id}",
    summary="Обновляет данные конкретного читателя",
    description=(
        """Этот эндпоинт редактирует информацию об читателе по его id. 
        Ожидает id читателя и необязательные данные для обновления: имя и email. 
        Возвращает статус операции и данные читателя c обновленными значениями."""
    ),
)
async def edit_reader(user: UserDep, db: DBDep, user_data: UserPatch):
    logger.info(f"Обновление данных пользователя с id: {user.id}")
    try:
        edited_user = await UserService(db).edit_user(user_data=user_data, id=user.id)
        logger.info(f"Данные пользователя с id: {user.id} успешно обновлены")
    except InvalidInputException:
        logger.error(f"Ошибка обновления данных пользователя с id: {user.id}: неверный ввод")
        raise InvalidInputHTTPException
    return {"status": "OK", "data": edited_user}
