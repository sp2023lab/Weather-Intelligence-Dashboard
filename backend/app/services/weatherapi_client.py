from time import perf_counter
from typing import Any

import requests

from app.core.cache import CacheService
from app.core.cache_metrics import cache_metrics
from app.core.config import settings


class WeatherAPIClient:
    def __init__(self, cache: CacheService | None = None) -> None:
        self.base_url = settings.WEATHER_API_BASE_URL
        self.api_key = settings.WEATHER_API_KEY
        self.cache = cache or CacheService()

    @staticmethod
    def _normalise_location(location: str) -> str:
        return " ".join(location.strip().lower().split())

    def _get_weather_data(
        self,
        *,
        operation: str,
        endpoint: str,
        cache_key: str,
        params: dict[str, Any],
        ttl_seconds: int,
    ) -> dict:
        total_started = perf_counter()
        cache_lookup_ms = 0.0
        provider_ms = 0.0

        try:
            if settings.CACHE_ENABLED:
                cache_started = perf_counter()
                cached_data = self.cache.get_json(cache_key)
                cache_lookup_ms = (
                    perf_counter() - cache_started
                ) * 1000

                if cached_data is not None:
                    total_ms = (
                        perf_counter() - total_started
                    ) * 1000

                    cache_metrics.record(
                        operation,
                        cache_status="hit",
                        cache_lookup_ms=cache_lookup_ms,
                        total_duration_ms=total_ms,
                        provider_called=False,
                    )

                    return cached_data

                cache_status = "miss"
            else:
                cache_status = "bypass"

            provider_started = perf_counter()

            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=10,
            )
            response.raise_for_status()

            provider_ms = (
                perf_counter() - provider_started
            ) * 1000

            weather_data = response.json()

            if settings.CACHE_ENABLED:
                self.cache.set_json(
                    key=cache_key,
                    value=weather_data,
                    ttl_seconds=ttl_seconds,
                )

            total_ms = (
                perf_counter() - total_started
            ) * 1000

            cache_metrics.record(
                operation,
                cache_status=cache_status,
                cache_lookup_ms=cache_lookup_ms,
                provider_ms=provider_ms,
                total_duration_ms=total_ms,
                provider_called=True,
            )

            return weather_data

        except Exception:
            total_ms = (
                perf_counter() - total_started
            ) * 1000

            cache_metrics.record(
                operation,
                cache_status=(
                    "miss"
                    if settings.CACHE_ENABLED
                    else "bypass"
                ),
                cache_lookup_ms=cache_lookup_ms,
                provider_ms=provider_ms,
                total_duration_ms=total_ms,
                provider_called=True,
                error=True,
            )

            raise

    def get_current_weather(self, location: str) -> dict:
        normalised_location = self._normalise_location(location)

        return self._get_weather_data(
            operation="current_weather",
            endpoint="current.json",
            cache_key=f"weather:current:{normalised_location}",
            params={
                "key": self.api_key,
                "q": location,
                "aqi": "yes",
            },
            ttl_seconds=settings.CURRENT_WEATHER_CACHE_TTL_SECONDS,
        )

    def get_forecast(self, location: str, days: int = 5) -> dict:
        normalised_location = self._normalise_location(location)

        return self._get_weather_data(
            operation="forecast",
            endpoint="forecast.json",
            cache_key=(
                f"weather:forecast:{normalised_location}:{days}"
            ),
            params={
                "key": self.api_key,
                "q": location,
                "days": days,
                "aqi": "yes",
                "alerts": "yes",
            },
            ttl_seconds=settings.FORECAST_CACHE_TTL_SECONDS,
        )