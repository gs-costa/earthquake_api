from datetime import datetime

from fastapi import APIRouter, Query, Request

from src.app.config.params import validate_date_format
from src.app.database.models import Features
from src.app.domains.features.schema import FeaturesResponse
from src.app.repositories.database_repository import DatabaseRepository

features_router = APIRouter(prefix="/features", tags=["features"])


@features_router.get("/", response_model=list[FeaturesResponse])
def get_features(
    request: Request,
    start_time: str = Query(description="Start time in YYYY-MM-DD format"),
    end_time: str = Query(description="End time in YYYY-MM-DD format"),
):
    """
    Get earthquake features within a date range.

    Args:
        request: FastAPI request object
        start_time: Start date in YYYY-MM-DD format
        end_time: End date in YYYY-MM-DD format

    Returns:
        JSON response with list of earthquake features within the specified date range
    """
    # Validate date format
    validate_date_format(start_time, end_time)

    database_repository = DatabaseRepository(Features, request.state.db_session)

    start_time_fmt = datetime.strptime(start_time, "%Y-%m-%d")
    end_time_fmt = datetime.strptime(end_time, "%Y-%m-%d")

    features = database_repository.get_by_date_range(
        date_column="time", start_time=start_time_fmt, end_time=end_time_fmt, order_by="time", order="desc"
    )

    features_json = [FeaturesResponse.model_validate(feature) for feature in features]

    return features_json
