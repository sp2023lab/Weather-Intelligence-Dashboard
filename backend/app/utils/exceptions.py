from fastapi import HTTPException
from requests import HTTPError, RequestException


def handle_weather_api_error(error: Exception):
    if isinstance(error, HTTPError):
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
            detail="Weather provider returned an error.",
        )

    if isinstance(error, RequestException):
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the weather provider.",
        )

    raise error