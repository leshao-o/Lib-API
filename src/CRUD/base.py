from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound, IntegrityError, ProgrammingError

from src.exceptions import InvalidInputException, ObjectNotFoundException


class BaseCRUD:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    # Метод для добавления данных в базу
    async def create(self, data: BaseModel) -> BaseModel:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(stmt)
        except IntegrityError:
            raise InvalidInputException
        # Валидация (приведение результата к pydantic модели) и возврат добавленной модели
        model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        return model

    # Метод для получения всех данных из таблицы
    async def get_all(self) -> list[BaseModel]:
        try:
            query = select(self.model)
            result = await self.session.execute(query)
            models = [
                self.schema.model_validate(one, from_attributes=True)
                for one in result.scalars().all()
            ]
            return models
        except NoResultFound:
            raise ObjectNotFoundException

    # Метод для получения данных по ID
    async def get_by_id(self, id: int) -> BaseModel:
        try:
            query = select(self.model).filter(self.model.id == id)
            result = await self.session.execute(query)
            model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
            return model
        except NoResultFound:
            raise ObjectNotFoundException

    # Метод для получения данных по фильтру
    async def get_filtered(self, **filter_by) -> list[BaseModel]:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        models = [
            self.schema.model_validate(one, from_attributes=True) for one in result.scalars().all()
        ]
        return models

    # Метод для изменения данных, которые передали
    async def update(self, data: BaseModel, **filter_by) -> BaseModel:
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        try:
            result = await self.session.execute(stmt)
        except (IntegrityError, ProgrammingError):
            raise InvalidInputException

        try:
            model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        except NoResultFound:
            raise ObjectNotFoundException

        return model

    # Метод для удаления данных по заданным фильтрам
    async def delete(self, **filter_by) -> BaseModel:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        try:
            model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        except NoResultFound:
            raise ObjectNotFoundException
        return model
