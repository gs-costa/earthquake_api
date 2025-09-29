"""
USGS Earthquake API client for fetching earthquake data.
"""

from datetime import date, datetime
from typing import Any

import requests

from ..api.base_api import BaseAPIClient


class USGSEarthquakeClient(BaseAPIClient):
    """
    Client for interacting with the USGS Earthquake API.

    This client provides methods to query earthquake data from the USGS FDSN Event API.
    """

    BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1"

    def __init__(self, default_headers: dict[str, str] | None = None):
        """
        Initialize the USGS Earthquake API client.

        Args:
            default_headers (Optional[Dict[str, str]]): Default headers to include in all requests
        """
        headers = {"User-Agent": "Earthquake-API-Client/1.0", "Accept": "application/json", **(default_headers or {})}

        super().__init__(self.BASE_URL, headers)

    def _format_date(self, date_input: Any) -> str:
        """
        Format date input to string format expected by USGS API.

        Args:
            date_input: Date as string, datetime object, or date object

        Returns:
            str: Formatted date string (YYYY-MM-DD)
        """
        if isinstance(date_input, str):
            return date_input
        elif isinstance(date_input, (datetime, date)):
            return date_input.strftime("%Y-%m-%d")
        else:
            raise ValueError(f"Invalid date format: {date_input}")

    def _format_datetime(self, datetime_input: Any) -> str:
        """
        Format datetime input to string format expected by USGS API.

        Args:
            datetime_input: Datetime as string, datetime object, or date object

        Returns:
            str: Formatted datetime string (YYYY-MM-DDTHH:MM:SS)
        """
        if isinstance(datetime_input, str):
            return datetime_input
        elif isinstance(datetime_input, datetime):
            return datetime_input.strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(datetime_input, date):
            return datetime_input.strftime("%Y-%m-%dT00:00:00")
        else:
            raise ValueError(f"Invalid datetime format: {datetime_input}")

    def query_earthquakes(
        self,
        start_time: Any,
        end_time: Any,
        format_type: str = "geojson",
        **kwargs,
    ) -> requests.Response:
        """
        Query earthquakes from the USGS API.

        Args:
            start_time: Start time for the query (string, datetime, or date)
            end_time: End time for the query (string, datetime, or date)
            format_type: Response format ('geojson', 'json', 'xml', 'csv', 'text')
            **kwargs: Additional query parameters (check https://earthquake.usgs.gov/fdsnws/event/1/#parameters for all possible parameters)

        Returns:
            requests.Response: The API response

        Raises:
            requests.RequestException: If the request fails
            ValueError: If date formats are invalid
        """

        params = {
            "format": format_type,
            "starttime": self._format_datetime(start_time),
            "endtime": self._format_datetime(end_time),
        }

        params.update(kwargs)

        return self.get("query", params=params)
