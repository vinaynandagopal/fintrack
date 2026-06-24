def test_list_categories(client):
    response = client.get("/api/categories")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 10