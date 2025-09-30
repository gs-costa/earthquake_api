import uuid
from datetime import datetime

from src.api.clients.usgs_earthquake_client import USGSEarthquakeClient
from src.app.database.config import SessionLocal
from src.app.database.models import Metadata
from src.app.repositories.database_repository import DatabaseRepository
from src.logger import Logger


class EarthquakeUSGSETL:
    logger = Logger(__name__)

    def __init__(self):
        self.client = USGSEarthquakeClient()
        self.db_session = SessionLocal()

    def ingest_metadata(self, metadata: dict) -> uuid.UUID:
        generated_timestamp = unix_timestamp_to_datetime(metadata.get("generated", 0))

        metadata_db = Metadata(
            generated=generated_timestamp,
            url=metadata.get("url", ""),
            title=metadata.get("title", ""),
            status=metadata.get("status", 0),
            api=metadata.get("api", ""),
            count=metadata.get("count", 0),
        )
        metadata_repository = DatabaseRepository(Metadata, self.db_session)
        try:
            metadata_repository.create(metadata_db)
            return metadata_db.id
        except Exception as e:
            self.logger.error(f"Error ingesting metadata: {e}")
            raise e

    def main(self, start_time: str, end_time: str):
        """Main function demonstrating USGS Earthquake API usage."""

        try:
            response = self.client.query_earthquakes(start_time=start_time, end_time=end_time, format_type="geojson")

            if response.status_code == 200:
                data = response.json()
                self.logger.info(f"Total earthquakes found: {data.get('metadata', {}).get('count', 0)}")

                metadata_id = self.ingest_metadata(data.get("metadata", {}))
                self.logger.info(f"Metadata ingested with ID: {metadata_id}")
            else:
                self.logger.error(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")

        finally:
            self.client.close()


def unix_timestamp_to_datetime(unix_timestamp: int) -> datetime:
    return datetime.fromtimestamp(unix_timestamp / 1000)


if __name__ == "__main__":
    EarthquakeUSGSETL().main(start_time="2024-01-01", end_time="2024-01-02")
