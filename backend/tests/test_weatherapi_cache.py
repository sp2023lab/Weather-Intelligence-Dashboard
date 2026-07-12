from unittest.mock import MagicMock

from app.services.weatherapi_client import WeatherAPIClient


def test_forecast_cache_hit_skips_external_request(monkeypatch):
    cached_payload = {
        "location": {"name": "London"},
        "forecast": {"forecastday": []},
    }

    cache = MagicMock()
    cache.get_json.return_value = cached_payload

    requests_get = MagicMock()

    monkeypatch.setattr(
        "app.services.weatherapi_client.requests.get",
        requests_get,
    )

    client = WeatherAPIClient(cache=cache)

    result = client.get_forecast("London", days=5)

    assert result == cached_payload

    cache.get_json.assert_called_once_with(
        "weather:forecast:london:5"
    )

    requests_get.assert_not_called()


def test_forecast_cache_miss_calls_provider_and_caches_response(
    monkeypatch,
):
    provider_payload = {
        "location": {"name": "London"},
        "forecast": {"forecastday": []},
    }

    cache = MagicMock()
    cache.get_json.return_value = None

    response = MagicMock()
    response.json.return_value = provider_payload

    requests_get = MagicMock(return_value=response)

    monkeypatch.setattr(
        "app.services.weatherapi_client.requests.get",
        requests_get,
    )

    client = WeatherAPIClient(cache=cache)

    result = client.get_forecast("London", days=5)

    assert result == provider_payload

    requests_get.assert_called_once()
    response.raise_for_status.assert_called_once()

    cache.set_json.assert_called_once_with(
        key="weather:forecast:london:5",
        value=provider_payload,
        ttl_seconds=1800,
    )


def test_current_weather_cache_normalises_location(monkeypatch):
    cached_payload = {
        "location": {"name": "New York"},
        "current": {"temp_c": 25},
    }

    cache = MagicMock()
    cache.get_json.return_value = cached_payload

    requests_get = MagicMock()

    monkeypatch.setattr(
        "app.services.weatherapi_client.requests.get",
        requests_get,
    )

    client = WeatherAPIClient(cache=cache)

    result = client.get_current_weather("  New   York  ")

    assert result == cached_payload

    cache.get_json.assert_called_once_with(
        "weather:current:new york"
    )

    requests_get.assert_not_called()