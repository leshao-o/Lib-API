from sqlalchemy import delete, insert, select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from src.exceptions import InvalidInputException, ObjectNotFoundException
from src.schemas.book import Book, BookWithRels, BooksAuthors, BooksAuthorsAdd
from src.models.book import BooksAuthorsORM, BooksORM
from src.CRUD.base import BaseCRUD
from src.logger import logger


class BookCRUD(BaseCRUD):
    model = BooksORM
    schema = Book

    async def get_book_with_rels(self, **filter_by) -> list[Book]:
        logger.info("Получение книг")
        query = select(self.model).options(selectinload(self.model.authors)).filter_by(**filter_by)
        result = await self.session.execute(query)
        models = [
            BookWithRels.model_validate(one, from_attributes=True) for one in result.scalars().all()
        ]
        if not models:
            logger.error("Книги не найдены")
            raise ObjectNotFoundException
        logger.info("Книги получены успешно")
        return models


class BooksAuthorsCRUD(BaseCRUD):
    model = BooksAuthorsORM
    schema = BooksAuthors

    async def add_many(self, data: list[BooksAuthorsAdd]) -> list[BooksAuthors]:
        logger.info("Добавление авторов книг")
        stmt = insert(self.model).values([item.model_dump() for item in data])
        try:
            await self.session.execute(stmt)
            logger.info("Авторы книг добавлены успешно")
        except IntegrityError:
            logger.error("Ошибка добавления авторов книг")
            raise InvalidInputException

    async def edit_authors_ids(self, new_authors_ids: list[int] | None, book_id: int) -> None:
        logger.info("Изменение авторов книги")
        new_authors_ids = new_authors_ids or []
        get_current_authors_ids_query = select(self.model.author_id).filter_by(book_id=book_id)
        result = await self.session.execute(get_current_authors_ids_query)
        current_authors_ids = result.scalars().all()
        ids_to_delete = list(set(current_authors_ids) - set(new_authors_ids))
        ids_to_insert = list(set(new_authors_ids) - set(current_authors_ids))

        try:
            if ids_to_delete:
                delete_stmt = delete(self.model).filter(
                    self.model.book_id == book_id, self.model.author_id.in_(ids_to_delete)
                )
                await self.session.execute(delete_stmt)

            if ids_to_insert:
                insert_stmt = insert(self.model).values(
                    [{"book_id": book_id, "author_id": a_id} for a_id in ids_to_insert]
                )
                await self.session.execute(insert_stmt)
            logger.info("Авторы книги изменены успешно")
        except IntegrityError:
            logger.error("Ошибка изменения авторов книги")
            raise InvalidInputException
