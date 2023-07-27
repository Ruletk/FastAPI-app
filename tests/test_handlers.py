import json


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
    users_from_db = dict(users_from_db[0])
    assert users_from_db["nickname"] == user_data["nickname"]
    assert users_from_db["email"] == user_data["email"]
    assert users_from_db["is_active"] is True
    assert str(users_from_db["user_id"]) == data_from_response["user_id"]
