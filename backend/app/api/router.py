from fastapi import APIRouter

from app.api.routes import export, health, metrics, weather


api_router = APIRouter()

api_router.include_router(weather.router)
api_router.include_router(export.router)
api_router.include_router(health.router)
api_router.include_router(metrics.router)