from datetime import date
import typing

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.book import BooksORM


class AuthorsORM(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    biography: Mapped[str] = mapped_column(String(300))
    birth_date: Mapped[date]

    books: Mapped[list["BooksORM"]] = relationship(
        back_populates="authors",
        secondary="books_authors"
    )
    