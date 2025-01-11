from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class BooksORM(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(300))
    date_of_publication: Mapped[date]
    author_id: Mapped[list[int]] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    genre: Mapped[str] = mapped_column(String(50))
    available_copies: Mapped[int]
