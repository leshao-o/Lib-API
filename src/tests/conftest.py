from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import insert

from src.services.auth import AuthService
from src.models.user import UsersORM
from src.database import Base, engine
from src.config import settings
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def check_test_mode() -> None:
    assert settings.MODE == "TEST"
    assert settings.DB_NAME == "test_db"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def user_ac(setup_database, ac: AsyncClient) -> AsyncGenerator[AsyncClient, None]:
    await ac.post(
        url="/auth/register",
        json={"name": "user", "email": "user@test.com", "password": "user"},
    )
    await ac.post(url="/auth/login", json={"email": "user@test.com", "password": "123456"})
    assert ac.cookies["access_token"]
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
