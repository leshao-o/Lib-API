from pydantic import EmailStr
from sqlalchemy import select

from src.schemas.user import User
from src.models.user import UsersORM
from src.CRUD.base import BaseCRUD


class UserCRUD(BaseCRUD):
    model = UsersORM
    schema = User

    async def get_user_by_email(self, email: EmailStr) -> User:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        # обработать ошибку когда нет юзера с таким email
        model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        return model
