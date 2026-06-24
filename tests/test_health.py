def test_health_api(client):
    response = client.get("/api/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["message"] == "FinTrack backend is running"