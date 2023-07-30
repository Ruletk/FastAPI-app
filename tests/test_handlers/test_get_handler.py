import uuid
import json


async def test_get_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid.uuid4(),
        "nickname": "Aboba",
        "email": "aboba@gmail.com",
        "is_active": True,
    }
    await create_user_in_database(**user_data)
    resp = client.get(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    data = resp.json()

    users_from_db = await get_user_from_database(user_data["user_id"])
    assert len(users_from_db) == 1

    assert user_data["nickname"] == data["nickname"]
    assert user_data["email"] == data["email"]
    assert user_data["is_active"] == data["is_active"]
    assert str(user_data["user_id"]) == str(data["user_id"])


async def test_unknown_users(client):
    for _ in range(10):
        user_id = uuid.uuid4()
        res = client.get(f"/user/?user_id={user_id}")
        assert res.status_code == 404


async def test_not_uuid(client):
    user_id = "ghjdfghjhgfghjkdfgdhjkhdfgjkhjkdgfhjkdgfhjk"
    res = client.get(f"/user/?user_id={user_id}")
    data = res.json()
    assert res.status_code == 422
    assert data == {
        "detail": [
            {
                "loc": ["query", "user_id"],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid",
            }
        ]
    }
