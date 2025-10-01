import uuid
from datetime import datetime

from pydantic import BaseModel


class EarthquakeMapPoint(BaseModel):
    """Pydantic model for earthquake map visualization data"""

    id: uuid.UUID
    latitude: float
    longitude: float
    mag: float | None = None
    place: str | None = None
    time: datetime | None = None
    depth: float | None = None
    event_id: str
    tsunami: int | None = None
    alert: str | None = None

    class Config:
        from_attributes = True


class EarthquakeMapResponse(BaseModel):
    """Response model for earthquake map data"""

    earthquakes: list[EarthquakeMapPoint]
    total_count: int
    date_range: dict[str, str]
