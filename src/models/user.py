from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text

from src.database import Base


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    
    is_user: Mapped[bool] = mapped_column(default=True, server_default=text("true"))
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text("false"))
