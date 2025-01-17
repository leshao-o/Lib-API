from httpx import AsyncClient


async def test_add_author(admin_ac: AsyncClient):
    response = await admin_ac.post(
        "/authors",
        json={
            "name": "test",
            "biography": "test",
            "birth_date": "2000-01-01"
        }
    )
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "test"
    assert response.json()["data"]["biography"] == "test"
    assert response.json()["data"]["birth_date"] == "2000-01-01"

async def test_get_authors(admin_ac: AsyncClient):
    response = await admin_ac.get("/authors")
    assert response.status_code == 200

async def test_get_author_by_id(admin_ac: AsyncClient):
    response = await admin_ac.get("/authors/1")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 1

async def test_edit_author(admin_ac: AsyncClient):
    response = await admin_ac.put(
        "/authors/1",
        json={
            "name": "test_1",
            "biography": "test_1",
            "birth_date": "2000-11-11"
        }
    )
    assert response.json()["data"]["name"] == "test_1"
    assert response.json()["data"]["biography"] == "test_1"
    assert response.json()["data"]["birth_date"] == "2000-11-11"

async def test_delete_author(admin_ac: AsyncClient):
    response = await admin_ac.delete("/authors/1")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 1
    