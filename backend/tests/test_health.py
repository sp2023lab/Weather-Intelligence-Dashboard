from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Weather API is running."
    assert response.json()["docs"] == "/docs"


def test_health_check():
    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "Weather API"
    assert response.json()["version"] == "1.0.0"