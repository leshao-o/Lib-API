from datetime import date

from fastapi import HTTPException

from src.schemas.user import User
from src.schemas.borrow import Borrow, BorrowAdd, BorrowAddRequest
from src.services.base import BaseService


class BorrowService(BaseService):
    async def add_borrow(self, borrow_data: BorrowAddRequest, user: User) -> Borrow:
        book = await self.db.book.get_by_id(id=borrow_data.book_id)

        if book.available_copies <= 0:
            raise HTTPException(status_code=404, detail="нет доступных книг")
        book.available_copies -= 1

        if user.borrowed_books >= 5:
            raise HTTPException(status_code=403, detail="занято максимальное количество книг")
        user.borrowed_books += 1

        _borrow_data = BorrowAdd(reader_id=user.id, **borrow_data.model_dump())
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
        if borrow.is_returned:
            raise HTTPException(status_code=403, detail="книга уже возвращена")
        
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
