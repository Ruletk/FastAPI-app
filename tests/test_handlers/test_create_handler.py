import json

import pytest


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


async def test_nickname_duplicate(client):  # WIP!
    user_data1 = {"nickname": "keyboard", "email": "keyboard@mail.ru"}
    # user_data2 = {"nickname": "keyboard", "email": "fgdhgfddfg@gmail.com"}

    resp = client.post("/user/", data=json.dumps(user_data1))
    assert resp.status_code == 200

    # resp_another = client.post("/user/", data=json.dumps(user_data2))


@pytest.mark.parametrize(
    "user_data, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "nickname"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "email"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ]
            },
        ),
        (
            {"nickname": "Aboba"},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            {"email": "dsafaf@gmail.com"},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "nickname"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        ),
        (
            {"nickname": "", "email": "dsafaf@gmail.com"},
            422,
            {"detail": "Nickname should contain 3 or more characters"},
        ),
        (
            {"nickname": "412412412421", "email": "dsafaf@gmail.com"},
            422,
            {
                "detail": "Nickname should start with a letter and contain only letters, numbers and underscores"
            },
        ),
        (
            {"nickname": "UserName", "email": "@gmail.com"},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email",
                    }
                ]
            },
        ),
    ],
)
async def test_create_user_error(
    client, user_data, expected_status_code, expected_detail
):
    resp = client.post("/user/", data=json.dumps(user_data))
    data = resp.json()
    assert resp.status_code == expected_status_code
    assert data == expected_detail
