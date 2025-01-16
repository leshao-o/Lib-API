from datetime import date

from pydantic import BaseModel


class BorrowAdd(BaseModel):
    reader_id: int
    book_id: int
    borrow_date: date
    return_date: date


class Borrow(BorrowAdd):
    id: int
