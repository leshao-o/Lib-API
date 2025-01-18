from typing import AsyncGenerator
from httpx import AsyncClient
import pytest


# Дополнительная фикстура для тестирования auth api, которая будет создавать пользователя 
# и авторизовывать его, чтобы когда будет тестироваться test_logout мы не
# потеряли access_token у основного admin_ac, который используется в других тестах
@pytest.fixture(scope="session")
async def auth_ac(setup_database, ac) -> AsyncGenerator[AsyncClient, None]:
    await ac.post(
        url="/auth/register",
        json={"name": "str", "email": "string@test.com", "password": "str"},
    )
    await ac.post(url="/auth/login", json={"email": "string@test.com", "password": "str"})
    assert ac.cookies["access_token"]
    yield ac
    
async def test_register_user(ac: AsyncClient):
    response = await ac.post(
        url="/auth/register",
        json={"name": "name", "email": "user@example.com", "password": "string"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "name"
    assert response.json()["data"]["email"] == "user@example.com"

async def test_login_user(auth_ac: AsyncClient):
    response = await auth_ac.post(
        url="/auth/login",
        json={"email": "string@test.com", "password": "str"},
    )
    assert response.status_code == 200
    assert response.cookies["access_token"]

async def test_get_me(auth_ac: AsyncClient):
    response = await auth_ac.get(url="/auth/me")
    assert response.status_code == 200

async def test_logout(auth_ac: AsyncClient):
    response = await auth_ac.post(url="/auth/")
    assert response.status_code == 200
    assert not response.cookies 
    