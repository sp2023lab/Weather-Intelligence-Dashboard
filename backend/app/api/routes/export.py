from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.export_service import ExportService

router = APIRouter(
    prefix="/export",
    tags=["Export"],
)

export_service = ExportService()


@router.get("/json")
def export_json(db: Session = Depends(get_db)):
    return export_service.export_json(db)


@router.get("/csv")
def export_csv(db: Session = Depends(get_db)):
    return export_service.export_csv(db)