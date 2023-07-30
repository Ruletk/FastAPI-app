import uuid
import json


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid.uuid4(),
        "nickname": "Aboba",
        "email": "aboba@gmail.com",
        "is_active": True,
    }

    await create_user_in_database(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}

    user_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(user_from_db[0])
    assert user_from_db["user_id"] == user_data["user_id"]
    assert user_from_db["nickname"] == user_data["nickname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False

    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 404


async def test_delete_unknown_user(client):
    user_id = uuid.uuid4()
    res = client.delete(f"/user/?user_id={user_id}")
    assert res.status_code == 404
