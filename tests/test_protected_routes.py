from conftest import register_user, auth_headers


def test_dashboard_requires_login(client):
    response = client.get("/api/dashboard/summary")

    assert response.status_code == 401


def test_dashboard_summary_with_login(client):
    register_response, register_data, payload = register_user(client)
    token = register_data["data"]["token"]

    response = client.get(
        "/api/dashboard/summary",
        headers=auth_headers(token)
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert "total_income" in data["data"]
    assert "total_expense" in data["data"]
    assert "savings" in data["data"]