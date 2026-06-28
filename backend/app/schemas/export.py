from datetime import date, datetime

from pydantic import BaseModel


class ExportRecord(BaseModel):
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