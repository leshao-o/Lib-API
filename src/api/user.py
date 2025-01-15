from fastapi import APIRouter

from src.services.user import UserService
from src.api.dependencies import DBDep, AdminUserDep, PaginationDep


router = APIRouter(prefix="/user", tags=["Пользователи"])


@router.get(
    "/",
    summary="Получение списка пользователей",
    description="Получение списка всех пользователей. Только для админов",
)
async def get_all_users(user_data: AdminUserDep, db: DBDep, pagination: PaginationDep):
    users = await UserService(db).get_all_users()
    users = users[pagination.per_page * (pagination.page - 1) :][: pagination.per_page]
    return {"status": "OK", "data": users}
