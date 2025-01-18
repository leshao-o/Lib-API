import json
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel
import pytest
from sqlalchemy import insert

from src.schemas.user import UserAdd, UserRequestAdd
from src.schemas.author import AuthorAdd
from src.schemas.book import BookAdd
from src.schemas.borrow import BorrowAdd
from src.services.auth import AuthService
from src.models.user import UsersORM
from src.database import Base, engine
from src.config import settings
from src.main import app
from src.utils.db_manager import DBManager
from src.database import async_session_maker


@pytest.fixture(scope="session", autouse=True)
def check_test_mode() -> None:
    assert settings.MODE == "TEST"
    assert settings.DB_NAME == "test_db"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def create_test_data(setup_database):
    async def load_and_validate_data(file_path: str, schema: BaseModel) -> list[BaseModel]:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.loads(file.read())
            return [schema.model_validate(item) for item in data]
    
    user = await load_and_validate_data("src/tests/data/mock_users.json", UserRequestAdd)
    authors = await load_and_validate_data("src/tests/data/mock_authors.json", AuthorAdd)
    books = await load_and_validate_data("src/tests/data/mock_books.json", BookAdd)
    borrows = await load_and_validate_data("src/tests/data/mock_borrows.json", BorrowAdd)

    hashed_password = AuthService().hash_password(user[0].password)
    user = UserAdd(**user[0].model_dump(), hashed_password=hashed_password)

    async with DBManager(session_factory=async_session_maker) as db:
        await db.user.create(user)
        await db.author.add_many(authors)
        await db.book.add_many(books)
        await db.borrow.add_many(borrows)
        await db.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def admin_ac(setup_database, ac: AsyncClient) -> AsyncGenerator[AsyncClient, None]:
    hashed_password = AuthService().hash_password("admin")
    async with engine.begin() as conn:
        await conn.execute(
            insert(UsersORM).values(name="admin", email="admin@test.com", hashed_password=hashed_password, is_admin=True)
        )
    await ac.post(
        url="/auth/login",
        json={"email": "admin@test.com", "password": "admin"},
    )
    assert ac.cookies["access_token"]
    yield ac
