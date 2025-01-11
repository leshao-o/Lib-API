from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class AuthorsORM(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    biography: Mapped[str] = mapped_column(String(300))
    birth_date: Mapped[date]
