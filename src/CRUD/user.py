from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions import UserNotFoundException
from src.schemas.user import User
from src.models.user import UsersORM
from src.CRUD.base import BaseCRUD
from src.logger import logger


class UserCRUD(BaseCRUD):
    model = UsersORM
    schema = User

    async def get_user_by_email(self, email: EmailStr) -> User:
        logger.info("Получение пользователя по email")
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
            logger.info("Пользователь получен успешно")
        except NoResultFound:
            logger.error("Пользователь не найден")
            raise UserNotFoundException
        return model
