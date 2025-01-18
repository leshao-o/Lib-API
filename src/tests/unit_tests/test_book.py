from httpx import AsyncClient


async def test_add_book(admin_ac: AsyncClient):
    response_book = await admin_ac.post(
        "/books",
        json={
            "title": "test",
            "description": "test",
            "date_of_publication": "2000-01-01",
            "author_ids": [2],
            "genre": "test",
            "available_copies": 5
        }
    )
    assert response_book.status_code == 200
    assert response_book.json()["data"]["title"] == "test"
    assert response_book.json()["data"]["description"] == "test"
    assert response_book.json()["data"]["date_of_publication"] == "2000-01-01"
    assert response_book.json()["data"]["genre"] == "test"
    assert response_book.json()["data"]["available_copies"] == 5

async def test_get_books(admin_ac: AsyncClient):
    response = await admin_ac.get("/books")
    assert response.status_code == 200

async def test_get_book_by_id(admin_ac: AsyncClient):
    response = await admin_ac.get("/books/1")
    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == 1

async def test_edit_book(admin_ac: AsyncClient):
    response = await admin_ac.put(
        "/books/1",
        json={
            "title": "title",
            "description": "description",
            "genre": "genre",
        }
    )
    assert response.json()["data"][0]["title"] == "title"
    assert response.json()["data"][0]["description"] == "description"
    assert response.json()["data"][0]["genre"] == "genre"

async def test_delete_book(admin_ac: AsyncClient):
    response = await admin_ac.delete("/books/1")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 1
    