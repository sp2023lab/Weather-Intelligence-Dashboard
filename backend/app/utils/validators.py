from datetime import date


def validate_date_range(start_date: date, end_date: date) -> None:
    if end_date < start_date:
        raise ValueError("End date must be on or after the start date.")


def validate_location(location: str) -> None:
    if not location or not location.strip():
        raise ValueError("Location cannot be empty.")