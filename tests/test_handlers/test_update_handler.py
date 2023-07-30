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


async def test_update_user_check_one_is_updated(
    client, create_user_in_database, get_user_from_database
):
    user_data1 = {
        "user_id": uuid.uuid4(),
        "nickname": "Moderator",
        "email": "Moderator@email.com",
        "is_active": True,
    }
    user_data2 = {
        "user_id": uuid.uuid4(),
        "nickname": "Support",
        "email": "Support@email.com",
        "is_active": True,
    }
    user_data3 = {
        "user_id": uuid.uuid4(),
        "nickname": "noreply",
        "email": "noreply@email.com",
        "is_active": True,
    }
    user_data4 = {
        "user_id": uuid.uuid4(),
        "nickname": "developer",
        "email": "developer@gmail.com",
        "is_active": True,
    }

    users = [user_data1, user_data2, user_data3, user_data4]
    for user in users:
        await create_user_in_database(**user)

    update_user1_data = {"nickname": "Admin", "email": "admin@gmail.com"}

    resp = client.patch(
        f"/user/?user_id={user_data1['user_id']}", data=json.dumps(update_user1_data)
    )
    assert resp.status_code == 200

    res = dict((await get_user_from_database(user_data1["user_id"]))[0])
    assert update_user1_data["nickname"] == res["nickname"]
    assert update_user1_data["email"] == res["email"]

    for user in [user_data2, user_data3, user_data4]:
        user_id = user["user_id"]
        res = await get_user_from_database(user_id)
        data = dict(res[0])
        assert user == data
