from conftest import register_user


def test_register_user(client):
    response, data, payload = register_user(client)

    assert response.status_code == 201
    assert data["success"] is True
    assert data["message"] == "User registered successfully"
    assert "token" in data["data"]
    assert data["data"]["user"]["email"] == payload["email"]


def test_login_user(client):
    register_response, register_data, payload = register_user(client)

    response = client.post("/api/auth/login", json={
        "email": payload["email"],
        "password": payload["password"]
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["message"] == "Login successful"
    assert "token" in data["data"]


def test_login_with_wrong_password_fails(client):
    register_response, register_data, payload = register_user(client)

    response = client.post("/api/auth/login", json={
        "email": payload["email"],
        "password": "wrongpassword"
    })

    data = response.get_json()

    assert response.status_code == 401
    assert data["success"] is False