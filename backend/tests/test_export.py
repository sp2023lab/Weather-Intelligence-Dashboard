from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_export_json():
    response = client.get("/export/json")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_export_csv():
    response = client.get("/export/csv")

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]
    assert "weather_records.csv" in response.headers["content-disposition"]


def test_export_csv_has_headers():
    response = client.get("/export/csv")

    assert response.status_code == 200

    csv_text = response.text

    assert "ID" in csv_text
    assert "Location" in csv_text
    assert "Temperature" in csv_text
    assert "Condition" in csv_text