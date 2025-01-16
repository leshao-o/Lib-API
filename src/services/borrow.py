from datetime import date

from src.exceptions import (
    BookAlreadyReturnedException,
    BookNotFoundException,
    MaxBooksLimitExceededException,
    NoAvailableCopiesException,
    ObjectNotFoundException,
    check_date,
)
from src.schemas.user import User
from src.schemas.borrow import Borrow, BorrowAdd, BorrowAddRequest
from src.services.base import BaseService


class BorrowService(BaseService):
    async def add_borrow(self, borrow_data: BorrowAddRequest, user: User) -> Borrow:
        check_date(borrow_date=borrow_data.borrow_date, return_date=borrow_data.return_date)
        try:
            book = await self.db.book.get_by_id(id=borrow_data.book_id)
        except ObjectNotFoundException:
            raise BookNotFoundException

        if book.available_copies <= 0:
            raise NoAvailableCopiesException
        book.available_copies -= 1

        if user.borrowed_books >= 5:
            raise MaxBooksLimitExceededException
        user.borrowed_books += 1

        _borrow_data = BorrowAdd(reader_id=user.id, **borrow_data.model_dump(), is_returned=False)
        borrow = await self.db.borrow.create(data=_borrow_data)
        await self.db.book.update(id=book.id, data=book)
        await self.db.user.update(id=user.id, data=user)
        await self.db.commit()
        return borrow

    async def get_borrows(self) -> list[Borrow]:
        return await self.db.borrow.get_all()

    async def get_my_borrows(self, user_id: int) -> list[Borrow]:
        return await self.db.borrow.get_filtered(reader_id=user_id)

    async def return_book(self, id: int, return_date: date, user: User) -> Borrow:
        borrow = await self.db.borrow.get_by_id(id=id)
        check_date(borrow_date=borrow.borrow_date, return_date=return_date)
        if borrow.is_returned:
            raise BookAlreadyReturnedException

        book = await self.db.book.get_by_id(id=borrow.book_id)

        book.available_copies += 1
        borrow.return_date = return_date
        borrow.is_returned = True
        user.borrowed_books -= 1

        await self.db.book.update(id=book.id, data=book)
        await self.db.borrow.update(id=borrow.id, data=borrow)
        await self.db.user.update(id=user.id, data=user)

        await self.db.commit()
        return borrow
