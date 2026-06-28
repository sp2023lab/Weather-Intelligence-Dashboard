from sqlalchemy.orm import Session

from app.models.weather_record import WeatherRecord
from app.schemas.weather import WeatherCreate, WeatherUpdate


class WeatherRepository:
    """
    Database operations for weather records.
    """

    def create(
        self,
        db: Session,
        weather_data: WeatherCreate,
        api_data: dict,
    ) -> WeatherRecord:
        location_data = api_data["location"]
        current_data = api_data["current"]

        record = WeatherRecord(
            location=weather_data.location,
            latitude=location_data["lat"],
            longitude=location_data["lon"],
            start_date=weather_data.start_date,
            end_date=weather_data.end_date,
            temperature=current_data["temp_c"],
            feels_like=current_data["feelslike_c"],
            humidity=current_data["humidity"],
            wind_speed=current_data["wind_kph"],
            condition=current_data["condition"]["text"],
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    def get_all(self, db: Session) -> list[WeatherRecord]:
        return (
            db.query(WeatherRecord)
            .order_by(WeatherRecord.created_at.desc())
            .all()
        )

    def get_by_id(self, db: Session, record_id: int) -> WeatherRecord | None:
        return (
            db.query(WeatherRecord)
            .filter(WeatherRecord.id == record_id)
            .first()
        )

    def update(
        self,
        db: Session,
        record: WeatherRecord,
        update_data: WeatherUpdate,
        api_data: dict | None = None,
    ) -> WeatherRecord:
        update_fields = update_data.model_dump(exclude_unset=True)

        for field, value in update_fields.items():
            setattr(record, field, value)

        if api_data:
            location_data = api_data["location"]
            current_data = api_data["current"]

            record.latitude = location_data["lat"]
            record.longitude = location_data["lon"]
            record.temperature = current_data["temp_c"]
            record.feels_like = current_data["feelslike_c"]
            record.humidity = current_data["humidity"]
            record.wind_speed = current_data["wind_kph"]
            record.condition = current_data["condition"]["text"]

        db.commit()
        db.refresh(record)

        return record

    def delete(self, db: Session, record: WeatherRecord) -> None:
        db.delete(record)
        db.commit()