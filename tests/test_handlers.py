import json
import uuid


async def test_create_user(client, get_user_from_database):
    user_data = {
        "nickname": "Nikolai",
        "email": "lol@kek.com",
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_response = resp.json()
    assert resp.status_code == 200
    assert data_from_response["nickname"] == user_data["nickname"]
    assert data_from_response["email"] == user_data["email"]
    assert data_from_response["is_active"] is True

    users_from_db = await get_user_from_database(data_from_response["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["nickname"] == user_data["nickname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_response["user_id"]


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


async def test_get_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid.uuid4(),
        "nickname": "Ababa",
        "email": "ababa@gmail.com",
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
