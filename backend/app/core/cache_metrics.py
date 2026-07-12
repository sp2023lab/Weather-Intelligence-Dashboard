from __future__ import annotations

from collections import defaultdict
from threading import Lock
from typing import Any


class CacheMetrics:
    def __init__(self) -> None:
        self._lock = Lock()
        self._metrics: dict[str, dict[str, float | int]] = defaultdict(
            lambda: {
                "requests": 0,
                "cache_hits": 0,
                "cache_misses": 0,
                "cache_bypasses": 0,
                "provider_calls": 0,
                "errors": 0,
                "total_cache_lookup_ms": 0.0,
                "total_provider_ms": 0.0,
                "total_duration_ms": 0.0,
            }
        )

    def record(
        self,
        operation: str,
        *,
        cache_status: str,
        cache_lookup_ms: float = 0.0,
        provider_ms: float = 0.0,
        total_duration_ms: float,
        provider_called: bool,
        error: bool = False,
    ) -> None:
        with self._lock:
            values = self._metrics[operation]

            values["requests"] += 1
            values["total_cache_lookup_ms"] += cache_lookup_ms
            values["total_provider_ms"] += provider_ms
            values["total_duration_ms"] += total_duration_ms

            if cache_status == "hit":
                values["cache_hits"] += 1
            elif cache_status == "miss":
                values["cache_misses"] += 1
            elif cache_status == "bypass":
                values["cache_bypasses"] += 1

            if provider_called:
                values["provider_calls"] += 1

            if error:
                values["errors"] += 1

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            result: dict[str, Any] = {}

            for operation, values in self._metrics.items():
                requests = int(values["requests"])
                hits = int(values["cache_hits"])
                cache_attempts = hits + int(values["cache_misses"])

                result[operation] = {
                    **values,
                    "cache_hit_rate_percent": (
                        round((hits / cache_attempts) * 100, 2)
                        if cache_attempts
                        else 0.0
                    ),
                    "average_cache_lookup_ms": (
                        round(
                            float(values["total_cache_lookup_ms"]) / requests,
                            3,
                        )
                        if requests
                        else 0.0
                    ),
                    "average_provider_ms": (
                        round(
                            float(values["total_provider_ms"])
                            / int(values["provider_calls"]),
                            3,
                        )
                        if int(values["provider_calls"])
                        else 0.0
                    ),
                    "average_total_duration_ms": (
                        round(
                            float(values["total_duration_ms"]) / requests,
                            3,
                        )
                        if requests
                        else 0.0
                    ),
                    "provider_calls_avoided": hits,
                }

            return result

    def reset(self) -> None:
        with self._lock:
            self._metrics.clear()


cache_metrics = CacheMetrics()