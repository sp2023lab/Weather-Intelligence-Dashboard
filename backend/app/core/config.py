from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from the .env file.
    """

    # Weather API
    WEATHER_API_KEY: str
    WEATHER_API_BASE_URL: str = "https://api.weatherapi.com/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./weather.db"

    # Application
    APP_NAME: str = "Weather API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()