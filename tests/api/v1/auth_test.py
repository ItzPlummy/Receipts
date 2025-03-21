from tests.conftest import client

test_user = {
    "username": "Plummy",
    "email": "plummybeatsoff@gmail.com",
    "password": "test_password"
}

test_login_data = {
    "username": "plummybeatsoff@gmail.com",
    "password": "test_password"
}


def test_registration():
    response = client.post(
        "api/v1/auth/register",
        json=test_user
    )

    assert response.status_code == 201
    client.app_state["access_token_1"] = response.json()["access_token"]
    client.app_state["auth_headers"] = {"Authorization": f"Bearer {response.json()["access_token"]}"}


def test_login():
    response = client.post(
        "api/v1/auth",
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data=test_login_data
    )

    assert response.status_code == 202


def test_my_user():
    response = client.get(
        "api/v1/auth",
        headers=client.app_state["auth_headers"]
    )

    assert response.status_code == 200
    assert response.json()["username"] == test_user["username"]

    client.app_state["user_id"] = response.json()["id"]


def test_bad_requests():
    response = client.post(
        "api/v1/auth/register",
        json=test_user
    )

    assert response.status_code == 409

    response = client.post(
        "api/v1/auth",
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={"username": "plummybeatsoff@gmail.com", "password": "wrong_password"}
    )

    assert response.status_code == 401

    response = client.get(
        "api/v1/auth",
        headers={"Authorization": "Bearer wrong_jwt_token"}
    )

    assert response.status_code == 401
