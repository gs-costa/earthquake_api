import uuid
from datetime import datetime

from src.app.database.models import Features, Metadatas


def unix_timestamp_to_datetime(unix_timestamp: int) -> datetime:
    return datetime.fromtimestamp(unix_timestamp / 1000)


def create_metadata(metadata: dict) -> Metadatas:
    generated_timestamp = unix_timestamp_to_datetime(metadata.get("generated", 0))

    metadata_db = Metadatas(
        generated=generated_timestamp,
        url=metadata.get("url", ""),
        title=metadata.get("title", ""),
        status=metadata.get("status", 0),
        api=metadata.get("api", ""),
        count=metadata.get("count", 0),
    )
    return metadata_db


def create_feature(feature: dict, metadata_id: uuid.UUID) -> Features:
    properties = feature.get("properties", {})
    geometry = feature.get("geometry", {})
    coordinates = geometry.get("coordinates", [0, 0, 0])  # [longitude, latitude, depth]

    feature_db = Features(
        mag=properties.get("mag", 0),
        place=properties.get("place", ""),
        time=unix_timestamp_to_datetime(properties.get("time", 0)),
        updated=unix_timestamp_to_datetime(properties.get("updated", 0)),
        tz=properties.get("tz", 0),
        url=properties.get("url", ""),
        detail=properties.get("detail", ""),
        felt=properties.get("felt", 0),
        cdi=properties.get("cdi", 0),
        mmi=properties.get("mmi", 0),
        alert=properties.get("alert", ""),
        status=properties.get("status", ""),
        tsunami=properties.get("tsunami", 0),
        sig=properties.get("sig", 0),
        net=properties.get("net", ""),
        code=properties.get("code", ""),
        ids=properties.get("ids", ""),
        sources=properties.get("sources", ""),
        types=properties.get("types", ""),
        nst=properties.get("nst", 0),
        dmin=properties.get("dmin", 0),
        rms=properties.get("rms", 0),
        gap=properties.get("gap", 0),
        mag_type=properties.get("magType", ""),
        latitude=coordinates[1] if len(coordinates) > 1 else 0,  # latitude
        longitude=coordinates[0] if len(coordinates) > 0 else 0,  # longitude
        depth=coordinates[2] if len(coordinates) > 2 else 0,  # depth
        event_id=feature.get("id", ""),
        metadata_id=metadata_id,
    )
    return feature_db
