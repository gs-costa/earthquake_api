from datetime import datetime
from typing import Literal, TypeVar

from fastapi import Request
from pydantic import BaseModel

from src.app.config.params import validate_date_format
from src.app.database.models import Features
from src.app.repositories.database_repository import DatabaseRepository
from src.data_integration.earthquake_usgs import EarthquakeUSGSETL

T = TypeVar("T", bound=BaseModel)


class EarthquakeService:
    """
    Service class to handle common earthquake data operations.
    """

    def __init__(self, request: Request):
        self.request = request
        self.db_session = request.state.db_session

    def get_earthquake_data(
        self,
        start_time: str,
        end_time: str,
        response_model: type[T],
        order_by: str = "time",
        order: Literal["asc", "desc"] = "desc",
        fetch_new_data: bool = True,
    ) -> list[T]:
        """
        Get earthquake data within a date range with common processing.

        Args:
            start_time: Start date in YYYY-MM-DD format
            end_time: End date in YYYY-MM-DD format
            response_model: Pydantic model class for response formatting
            order_by: Column to order by (default: "time")
            order: Order direction (default: "desc")
            fetch_new_data: Whether to fetch new data from USGS API (default: True)

        Returns:
            List of formatted features
        """

        validate_date_format(start_time, end_time)

        if fetch_new_data:
            metadata_id = EarthquakeUSGSETL().main(start_time=start_time, end_time=end_time)
            self.request.state.metadata_id = metadata_id
        else:
            self.request.state.metadata_id = None

        database_repository = DatabaseRepository(Features, self.db_session)

        start_time_fmt = datetime.strptime(start_time, "%Y-%m-%d")
        end_time_fmt = datetime.strptime(end_time, "%Y-%m-%d")

        features = database_repository.get_by_date_range(
            date_column="time", start_time=start_time_fmt, end_time=end_time_fmt, order_by=order_by, order=order
        )

        formatted_features = [response_model.model_validate(feature) for feature in features]

        return formatted_features
