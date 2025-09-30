import uuid
from datetime import datetime

from src.api.clients.usgs_earthquake_client import USGSEarthquakeClient
from src.app.database.config import SessionLocal
from src.app.database.models import Features, Metadatas
from src.app.repositories.database_repository import DatabaseRepository
from src.logger import Logger


class EarthquakeUSGSETL:
    logger = Logger(__name__)

    def __init__(self):
        self.client = USGSEarthquakeClient()
        self.db_session = SessionLocal()

    def ingest_metadata(self, metadata: dict) -> uuid.UUID:
        generated_timestamp = unix_timestamp_to_datetime(metadata.get("generated", 0))

        metadata_db = Metadatas(
            generated=generated_timestamp,
            url=metadata.get("url", ""),
            title=metadata.get("title", ""),
            status=metadata.get("status", 0),
            api=metadata.get("api", ""),
            count=metadata.get("count", 0),
        )
        metadata_repository = DatabaseRepository(Metadatas, self.db_session)
        try:
            metadata_repository.create(metadata_db)
            return metadata_db.id  # type: ignore
        except Exception as e:
            self.logger.error(f"Error ingesting metadata: {e}")
            raise e

    def ingest_features(self, features: list[dict], metadata_id: uuid.UUID) -> None:
        """Ingest multiple features in bulk for better performance."""
        if not features:
            self.logger.warning("No features to ingest")
            return

        features_db_list = []
        for feature in features:
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
            features_db_list.append(feature_db)

        features_repository = DatabaseRepository(Features, self.db_session)
        try:
            created_features = features_repository.bulk_create(features_db_list)
            self.logger.info(f"Successfully ingested {len(created_features)} features")
        except Exception as e:
            self.logger.error(f"Error ingesting features: {e}")
            raise e

    def main(self, start_time: str, end_time: str):
        """Main function demonstrating USGS Earthquake API usage."""

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
            else:
                self.logger.error(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")

        finally:
            self.client.close()
            self.db_session.close()


def unix_timestamp_to_datetime(unix_timestamp: int) -> datetime:
    return datetime.fromtimestamp(unix_timestamp / 1000)


if __name__ == "__main__":
    EarthquakeUSGSETL().main(start_time="2025-01-01", end_time="2025-01-02")
