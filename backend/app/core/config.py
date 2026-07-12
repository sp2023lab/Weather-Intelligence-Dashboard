from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Application configuration loaded from the backend .env file.
    """

    # Weather API
    WEATHER_API_KEY: str
    WEATHER_API_BASE_URL: str = "https://api.weatherapi.com/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./weather.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_ENABLED: bool = True
    CURRENT_WEATHER_CACHE_TTL_SECONDS: int = 600
    FORECAST_CACHE_TTL_SECONDS: int = 1800

    # Application
    APP_NAME: str = "Weather API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=BACKEND_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()