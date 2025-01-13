from src.schemas.user import User
from src.models.user import UsersORM
from src.CRUD.base import BaseCRUD


class UserCRUD(BaseCRUD):
    model = UsersORM
    schema = User
