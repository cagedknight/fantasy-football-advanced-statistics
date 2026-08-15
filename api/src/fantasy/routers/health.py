from fastapi import APIRouter
from pydantic import BaseModel

from fantasy import __version__
from fantasy.config import get_settings

router = APIRouter(tags=["meta"])


class Health(BaseModel):
    status: str
    environment: str
    version: str


@router.get("/health", response_model=Health)
async def health() -> Health:
    """Liveness probe. Deployment targets poll this to decide if a release is good."""
    return Health(status="ok", environment=get_settings().environment, version=__version__)
