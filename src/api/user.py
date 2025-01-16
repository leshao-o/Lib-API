from fastapi import APIRouter

from src.schemas.user import UserPatch
from src.services.user import UserService
from src.api.dependencies import DBDep, AdminUserDep, PaginationDep, UserDep


router = APIRouter(prefix="/user", tags=["Пользователи"])


@router.get(
    "/",
    summary="Получение списка пользователей",
    description="Получение списка всех пользователей. Только для админов",
)
async def get_all_users(user: AdminUserDep, db: DBDep, pagination: PaginationDep):
    users = await UserService(db).get_all_users()
    users = users[pagination.per_page * (pagination.page - 1) :][: pagination.per_page]
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
    edited_user = await UserService(db).edit_user(user_data=user_data, id=user.id)
    return {"status": "OK", "data": edited_user}
