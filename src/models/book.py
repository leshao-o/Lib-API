from datetime import date
import typing

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.author import AuthorsORM


class BooksORM(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(300))
    date_of_publication: Mapped[date]
    genre: Mapped[str] = mapped_column(String(50))
    available_copies: Mapped[int]

    authors: Mapped[list["AuthorsORM"]] = relationship(
        back_populates="books", secondary="books_authors"
    )


class BooksAuthorsORM(Base):
    __tablename__ = "books_authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
