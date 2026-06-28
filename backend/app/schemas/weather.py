from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator


class WeatherCreate(BaseModel):
    """
    Request model for creating a weather record.
    """

    location: str = Field(..., min_length=1, max_length=255)
    start_date: date
    end_date: date

    @field_validator("end_date")
    @classmethod
    def validate_date_range(cls, end_date: date, info):
        start_date = info.data.get("start_date")

        if start_date and end_date < start_date:
            raise ValueError("End date must be on or after the start date.")

        return end_date


class WeatherUpdate(BaseModel):
    """
    Request model for updating a weather record.
    """

    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class WeatherResponse(BaseModel):
    """
    Response model returned to the client.
    """

    id: int

    location: str
    latitude: float
    longitude: float

    start_date: date
    end_date: date

    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    condition: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }