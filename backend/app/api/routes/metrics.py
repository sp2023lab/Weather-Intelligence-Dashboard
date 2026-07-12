from fastapi import APIRouter, Response

from app.core.cache_metrics import cache_metrics


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)


@router.get("/cache")
def get_cache_metrics():
    return cache_metrics.snapshot()


@router.delete("/cache", status_code=204)
def reset_cache_metrics():
    cache_metrics.reset()
    return Response(status_code=204)