from httpx import AsyncClient


async def test_get_all_users(admin_ac: AsyncClient):
    response = await admin_ac.get("/user/")
    assert response.status_code == 200

async def test_turn_user_to_admin(admin_ac: AsyncClient):
    response = await admin_ac.put(
        url="/user/1",
        json={"is_admin": True}
    )
    assert response.status_code == 200
    assert response.json()["data"]["is_admin"] == True

async def test_edit_reader(admin_ac: AsyncClient):
    response = await admin_ac.put(
        url="/user/edit/1",
        json={
            "name": "new_name",
            "email": "new_email@example.com"
        }
    )
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "new_name"
    assert response.json()["data"]["email"] == "new_email@example.com"
    