import uuid

from src.api.clients.usgs_earthquake_client import USGSEarthquakeClient
from src.app.database.config import SessionLocal
from src.app.database.models import Features, Metadatas
from src.app.repositories.database_repository import DatabaseRepository
from src.data_integration.helpers import create_feature, create_metadata
from src.logger import Logger


class EarthquakeUSGSETL:
    logger = Logger(__name__)

    def __init__(self):
        self.client = USGSEarthquakeClient()
        self.db_session = SessionLocal()

    def ingest_metadata(self, metadata: dict) -> uuid.UUID:
        metadata_db = create_metadata(metadata)
        metadata_repository = DatabaseRepository(Metadatas, self.db_session)
        try:
            metadata_repository.create(metadata_db)
            return metadata_db.id  # type: ignore
        except Exception as e:
            self.logger.error(f"Error ingesting metadata: {e}")
            raise e

    def ingest_features(self, features: list[dict], metadata_id: uuid.UUID) -> None:
        """Upsert features to database, updating existing records based on event_id."""
        if not features:
            self.logger.warning("No features to ingest")
            return

        features_db_list = []
        for feature in features:
            feature_db = create_feature(feature, metadata_id)
            features_db_list.append(feature_db)

        features_repository = DatabaseRepository(Features, self.db_session)
        try:
            upserted_count = features_repository.bulk_upsert(features_db_list, conflict_column="event_id")
            self.logger.info(f"Successfully upserted {upserted_count} features")
        except Exception as e:
            self.logger.error(f"Error upserting features: {e}")
            raise e

    def main(self, start_time: str, end_time: str):
        """Main function ingesting USGS Earthquake API data to database."""

        try:
            response = self.client.query_earthquakes(start_time=start_time, end_time=end_time, format_type="geojson")

            if response.status_code == 200:
                data = response.json()
                features = data.get("features", [])
                self.logger.info(f"Total earthquakes found: {data.get('metadata', {}).get('count', 0)}")

                metadata_id = self.ingest_metadata(data.get("metadata", {}))
                self.logger.info(f"Metadata ingested with ID: {metadata_id}")

                if features:
                    self.ingest_features(features, metadata_id)
                    self.logger.info(f"Successfully processed {len(features)} earthquake features")
                else:
                    self.logger.warning("No features found in the response")
                return metadata_id
            else:
                self.logger.error(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")

        finally:
            self.client.close()
            self.db_session.close()


if __name__ == "__main__":
    EarthquakeUSGSETL().main(start_time="2024-03-01", end_time="2024-03-02")
