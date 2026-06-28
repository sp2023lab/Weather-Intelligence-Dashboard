from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_weather_records():
    response = client.get("/weather/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_existing_weather_record():
    response = client.get("/weather/1")

    assert response.status_code in [200, 404]


def test_get_missing_weather_record():
    response = client.get("/weather/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Weather record not found."


def test_create_weather_record_invalid_date_range():
    response = client.post(
        "/weather/",
        json={
            "location": "London",
            "start_date": "2026-07-03",
            "end_date": "2026-06-28",
        },
    )

    assert response.status_code == 422


def test_create_weather_record_empty_location():
    response = client.post(
        "/weather/",
        json={
            "location": "",
            "start_date": "2026-06-28",
            "end_date": "2026-07-03",
        },
    )

    assert response.status_code == 422


def test_update_missing_weather_record():
    response = client.put(
        "/weather/999999",
        json={
            "location": "Manchester"
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Weather record not found."


def test_delete_missing_weather_record():
    response = client.delete("/weather/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Weather record not found."