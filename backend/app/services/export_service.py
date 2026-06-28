from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.repositories.weather_repository import WeatherRepository
from app.utils.csv_export import records_to_csv


class ExportService:
    def __init__(self):
        self.repository = WeatherRepository()

    def export_json(self, db: Session):
        return self.repository.get_all(db)

    def export_csv(self, db: Session):
        records = self.repository.get_all(db)
        csv_file = records_to_csv(records)

        return StreamingResponse(
            csv_file,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=weather_records.csv"
            },
        )