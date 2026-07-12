import json
import logging
from typing import Any

from redis import Redis
from redis.exceptions import RedisError

from app.core.config import settings


logger = logging.getLogger(__name__)


class CacheService:
    """
    JSON cache backed by Redis.

    Redis failures are treated as cache misses so that the application
    can continue using the external weather provider.
    """

    def __init__(self) -> None:
        self.client = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1,
        )

    def get_json(self, key: str) -> dict[str, Any] | None:
        if not settings.CACHE_ENABLED:
            return None

        try:
            cached_value = self.client.get(key)

            if cached_value is None:
                return None

            return json.loads(cached_value)

        except json.JSONDecodeError:
            logger.warning("Invalid JSON stored for Redis key %s", key)

            try:
                self.client.delete(key)
            except RedisError:
                pass

            return None

        except RedisError as error:
            logger.warning("Redis cache read failed: %s", error)
            return None

    def set_json(
        self,
        key: str,
        value: dict[str, Any],
        ttl_seconds: int,
    ) -> None:
        if not settings.CACHE_ENABLED:
            return

        try:
            self.client.set(
                name=key,
                value=json.dumps(value),
                ex=ttl_seconds,
            )

        except RedisError as error:
            logger.warning("Redis cache write failed: %s", error)

    def delete(self, key: str) -> None:
        if not settings.CACHE_ENABLED:
            return

        try:
            self.client.delete(key)
        except RedisError as error:
            logger.warning("Redis cache delete failed: %s", error)

    def ping(self) -> bool:
        if not settings.CACHE_ENABLED:
            return False

        try:
            return bool(self.client.ping())
        except RedisError:
            return False