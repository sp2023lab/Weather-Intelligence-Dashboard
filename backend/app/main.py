from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.database import Base, engine

from time import perf_counter

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React (Vite)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routes
app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "Weather API is running.",
        "docs": "/docs",
    }

@app.middleware("http")
async def add_process_time_header(
    request: Request,
    call_next,
):
    started = perf_counter()

    response = await call_next(request)

    duration_ms = (perf_counter() - started) * 1000
    response.headers["X-Process-Time-Ms"] = f"{duration_ms:.3f}"

    return response