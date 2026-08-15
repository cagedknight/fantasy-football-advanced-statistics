from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fantasy import __version__
from fantasy.config import get_settings
from fantasy.routers import health


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Fantasy API",
        version=__version__,
        summary="Free-agent valuation scored against your league's rules.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    return app


app = create_app()
