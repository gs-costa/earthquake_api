import uuid
from datetime import datetime

from pydantic import BaseModel


class FeaturesResponse(BaseModel):
    """Pydantic model for Features API response"""

    id: uuid.UUID
    mag: float | None = None
    place: str | None = None
    time: datetime | None = None
    updated: datetime | None = None
    tz: int | None = None
    url: str | None = None
    detail: str | None = None
    felt: int | None = None
    cdi: float | None = None
    mmi: float | None = None
    alert: str | None = None
    status: str | None = None
    tsunami: int | None = None
    sig: int | None = None
    net: str | None = None
    code: str | None = None
    ids: str | None = None
    sources: str | None = None
    types: str | None = None
    nst: int | None = None
    dmin: float | None = None
    rms: float | None = None
    gap: float | None = None
    mag_type: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    depth: float | None = None
    event_id: str
    metadata_id: uuid.UUID

    class Config:
        from_attributes = True
