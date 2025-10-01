from fastapi import APIRouter, Query, Request

from src.app.domains.earthquake_service import EarthquakeService
from src.app.domains.features.schema import FeaturesResponse

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
    earthquake_service = EarthquakeService(request)
    features_json = earthquake_service.get_earthquake_data(
        start_time=start_time, end_time=end_time, response_model=FeaturesResponse
    )

    return features_json
