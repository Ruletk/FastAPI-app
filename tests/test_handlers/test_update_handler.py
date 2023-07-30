import uuid
import json


async def test_update_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid.uuid4(),
        "nickname": "Aboba",
        "email": "aboba@gmail.com",
        "is_active": True,
    }
    updated_user_data = {"nickname": "Petr", "email": "petr@example.com"}
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}", data=json.dumps(updated_user_data)
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["user_id"] == user_data["user_id"]
    assert user_from_db["nickname"] == updated_user_data["nickname"]
    assert user_from_db["email"] == updated_user_data["email"]
    assert user_from_db["is_active"] == user_data["is_active"]
