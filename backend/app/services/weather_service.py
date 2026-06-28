from sqlalchemy.orm import Session

from app.repositories.weather_repository import WeatherRepository
from app.schemas.weather import WeatherCreate, WeatherUpdate
from app.services.weatherapi_client import WeatherAPIClient


class WeatherService:
    """
    Business logic for weather operations.
    """

    def __init__(self):
        self.weather_client = WeatherAPIClient()
        self.repository = WeatherRepository()

    def create_weather_record(
        self,
        db: Session,
        weather_request: WeatherCreate,
    ):
        """
        Create a new weather record.
        """

        api_data = self.weather_client.get_current_weather(
            weather_request.location
        )

        return self.repository.create(
            db=db,
            weather_data=weather_request,
            api_data=api_data,
        )

    def get_all_weather_records(
        self,
        db: Session,
    ):
        """
        Retrieve all stored weather records.
        """

        return self.repository.get_all(db)

    def get_weather_record(
        self,
        db: Session,
        record_id: int,
    ):
        """
        Retrieve a single weather record.
        """

        return self.repository.get_by_id(db, record_id)

    def update_weather_record(
        self,
        db: Session,
        record_id: int,
        update_request: WeatherUpdate,
    ):
        """
        Update an existing weather record.
        """

        record = self.repository.get_by_id(db, record_id)

        if record is None:
            return None

        api_data = None

        if update_request.location:
            api_data = self.weather_client.get_current_weather(
                update_request.location
            )

        return self.repository.update(
            db=db,
            record=record,
            update_data=update_request,
            api_data=api_data,
        )

    def delete_weather_record(
        self,
        db: Session,
        record_id: int,
    ):
        """
        Delete a weather record.
        """

        record = self.repository.get_by_id(db, record_id)

        if record is None:
            return False

        self.repository.delete(db, record)

        return True

    def get_forecast(
        self,
        location: str,
        days: int = 5,
    ):
        """
        Retrieve weather forecast.
        """

        return self.weather_client.get_forecast(location, days)