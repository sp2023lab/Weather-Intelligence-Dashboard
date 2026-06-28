import requests

from app.core.config import settings


class WeatherAPIClient:
    """
    Client for interacting with the WeatherAPI service.
    """

    def __init__(self):
        self.base_url = settings.WEATHER_API_BASE_URL
        self.api_key = settings.WEATHER_API_KEY

    def get_current_weather(self, location: str) -> dict:
        """
        Retrieve current weather for a location.
        """

        url = f"{self.base_url}/current.json"

        params = {
            "key": self.api_key,
            "q": location,
            "aqi": "yes",
        }

        response = requests.get(url, params=params, timeout=10)

        response.raise_for_status()

        return response.json()

    def get_forecast(self, location: str, days: int = 5) -> dict:
        """
        Retrieve forecast data.
        """

        url = f"{self.base_url}/forecast.json"

        params = {
            "key": self.api_key,
            "q": location,
            "days": days,
            "aqi": "yes",
            "alerts": "yes",
        }

        response = requests.get(url, params=params, timeout=10)

        response.raise_for_status()

        return response.json()