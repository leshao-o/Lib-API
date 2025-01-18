from httpx import AsyncClient


async def test_add_borrow(admin_ac: AsyncClient):
    response = await admin_ac.post(
        url="/borrows",
        json={
            "book_id": 2,
            "borrow_date": "2000-01-01",
            "return_date": "2000-01-02"
        }
    )
    assert response.status_code == 200
    assert response.json()["data"]["borrow_date"] == "2000-01-01"
    assert response.json()["data"]["return_date"] == "2000-01-02"
    assert response.json()["data"]["book_id"] == 2
    print(response.json())
    
async def test_get_borrows(admin_ac: AsyncClient):
    response = await admin_ac.get(url="/borrows")
    assert response.status_code == 200
    print(response.json())

async def test_get_my_borrows(admin_ac: AsyncClient):
    response = await admin_ac.get(url="/borrows/1")
    assert response.status_code == 200
    print(response.json())
    
async def test_return_book(admin_ac: AsyncClient):
    response = await admin_ac.patch(
        url="/borrows/1/return",
        params={
            "return_date": "2025-02-02",
        }
    )
    assert response.status_code == 200
    assert response.json()["data"]["is_returned"] == True
