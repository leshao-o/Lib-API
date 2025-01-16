from src.exceptions import BookNotFoundException, InvalidInputException, ObjectNotFoundException
from src.schemas.book import (
    Book,
    BookAdd,
    BookAddRequest,
    BookPatch,
    BooksAuthorsAdd,
    BookPatchRequest,
)
from src.services.base import BaseService


class BookService(BaseService):
    async def create_book(self, book_data: BookAddRequest) -> Book:
        if book_data.available_copies < 0:
            raise InvalidInputException

        _book_data = BookAdd(**book_data.model_dump())
        new_book = await self.db.book.create(data=_book_data)
        books_authors_data = [
            BooksAuthorsAdd(book_id=new_book.id, author_id=a_ids)
            for a_ids in set(book_data.author_ids)
        ]
        await self.db.books_authors.add_many(data=books_authors_data)
        await self.db.commit()
        return new_book

    async def get_books(self) -> list[Book]:
        return await self.db.book.get_book_with_rels()

    async def get_book_by_id(self, id: int) -> Book:
        return await self.db.book.get_book_with_rels(id=id)

    async def edit_book(self, id: int, book_data: BookPatchRequest) -> Book:
        _book_data = BookPatch(**book_data.model_dump(exclude_unset=True))
        try:
            if any(dict(_book_data).values()):
                edited_book = await self.db.book.update(id=id, data=_book_data)

            await self.db.books_authors.edit_authors_ids(
                book_id=id, new_authors_ids=book_data.author_ids
            )
            edited_book = await self.db.book.get_book_with_rels(id=id)
        except ObjectNotFoundException:
            raise BookNotFoundException

        await self.db.commit()
        return edited_book

    async def delete_book(self, id: int) -> Book:
        try:
            deleted_book = await self.db.book.delete(id=id)
        except ObjectNotFoundException:
            raise BookNotFoundException
        await self.db.commit()
        return deleted_book
