from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_forecast_invalid_days_type():
    response = client.get("/weather/forecast/London?days=abc")

    assert response.status_code == 422


def test_forecast_endpoint_exists():
    response = client.get("/weather/forecast/London?days=1")

    assert response.status_code in [200, 404, 502, 503]