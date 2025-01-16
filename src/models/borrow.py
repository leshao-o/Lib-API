from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class BorrowsORM(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    reader_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    borrow_date: Mapped[date]
    return_date: Mapped[date]
