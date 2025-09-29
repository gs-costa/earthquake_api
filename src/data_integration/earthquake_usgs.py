from datetime import datetime

from src.api.clients.usgs_earthquake_client import USGSEarthquakeClient
from src.app.database.config import SessionLocal
from src.app.database.models import Metadata
from src.app.repositories.database_repository import DatabaseRepository
from src.logger import Logger


def main(start_time: str, end_time: str):
    """Main function demonstrating USGS Earthquake API usage."""
    logger = Logger(__name__)

    client = USGSEarthquakeClient()

    db_session = SessionLocal()

    try:
        response = client.query_earthquakes(start_time=start_time, end_time=end_time, format_type="geojson")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Total earthquakes found: {data.get('metadata', {}).get('count', 0)}")

            metadata = data.get("metadata", {})

            generated_timestamp = unix_timestamp_to_datetime(metadata.get("generated", 0))

            metadata_db = Metadata(
                generated=generated_timestamp,
                url=metadata.get("url", ""),
                title=metadata.get("title", ""),
                status=metadata.get("status", 0),
                api=metadata.get("api", ""),
                count=metadata.get("count", 0),
            )
            metadata_repository = DatabaseRepository(Metadata, db_session)
            metadata_repository.create(metadata_db)
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"Error occurred: {e}")

    finally:
        client.close()


def unix_timestamp_to_datetime(unix_timestamp: int) -> datetime:
    return datetime.fromtimestamp(unix_timestamp / 1000)


if __name__ == "__main__":
    main(start_time="2024-01-01", end_time="2024-01-02")
