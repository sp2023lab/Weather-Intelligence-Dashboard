from fastapi import APIRouter, Depends, HTTPException
from requests import HTTPError, RequestException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.weather import WeatherCreate, WeatherResponse, WeatherUpdate
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])

weather_service = WeatherService()


@router.post("/", response_model=WeatherResponse, status_code=201)
def create_weather_record(
    weather_request: WeatherCreate,
    db: Session = Depends(get_db),
):
    try:
        return weather_service.create_weather_record(db, weather_request)

    except HTTPError as error:
        status_code = error.response.status_code if error.response else 502

        if status_code in {400, 404}:
            raise HTTPException(
                status_code=404,
                detail="Location not found. Please check the spelling or try a more specific location.",
            )

        if status_code in {401, 403}:
            raise HTTPException(
                status_code=502,
                detail="Weather provider authentication failed.",
            )

        raise HTTPException(
            status_code=502,
            detail=error.response.text if error.response else "Weather provider returned an error.",
        )

    except RequestException:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the weather provider.",
        )


@router.get("/", response_model=list[WeatherResponse])
def get_all_weather_records(db: Session = Depends(get_db)):
    return weather_service.get_all_weather_records(db)


@router.get("/{record_id}", response_model=WeatherResponse)
def get_weather_record(
    record_id: int,
    db: Session = Depends(get_db),
):
    record = weather_service.get_weather_record(db, record_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Weather record not found.",
        )

    return record


@router.put("/{record_id}", response_model=WeatherResponse)
def update_weather_record(
    record_id: int,
    update_request: WeatherUpdate,
    db: Session = Depends(get_db),
):
    try:
        record = weather_service.update_weather_record(
            db,
            record_id,
            update_request,
        )

        if record is None:
            raise HTTPException(
                status_code=404,
                detail="Weather record not found.",
            )

        return record

    except HTTPError as error:
        status_code = error.response.status_code if error.response else 502

        if status_code in {400, 404}:
            raise HTTPException(
                status_code=404,
                detail="Updated location was not found.",
            )

        raise HTTPException(
            status_code=502,
            detail="Weather provider returned an error.",
        )

    except RequestException:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the weather provider.",
        )


@router.delete("/{record_id}", status_code=204)
def delete_weather_record(
    record_id: int,
    db: Session = Depends(get_db),
):
    deleted = weather_service.delete_weather_record(db, record_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Weather record not found.",
        )

    return None


@router.get("/forecast/{location}")
def get_forecast(location: str, days: int = 5):
    try:
        return weather_service.get_forecast(location, days)

    except HTTPError:
        raise HTTPException(
            status_code=404,
            detail="Forecast location not found.",
        )

    except RequestException:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the weather provider.",
        )