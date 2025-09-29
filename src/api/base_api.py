"""
Base API client for making HTTP requests with configurable headers and parameters.
"""

from typing import Any
from urllib.parse import urlencode

import requests

from ..logger import Logger


class BaseAPIClient:
    """
    Base class for API clients that provides common HTTP request functionality.

    This class handles making HTTP requests with configurable headers and parameters,
    providing a foundation for specific API clients.
    """

    logger = Logger(__name__)

    def __init__(self, base_url: str, default_headers: dict[str, str] | None = None):
        """
        Initialize the base API client.

        Args:
            base_url (str): The base URL for the API
            default_headers (Optional[Dict[str, str]]): Default headers to include in all requests
        """
        self.base_url = base_url.rstrip("/")
        self.default_headers = default_headers or {}
        self.session = requests.Session()

        if self.default_headers:
            self.session.headers.update(self.default_headers)

    def _build_url(self, endpoint: str, params: dict[str, Any] | None = None) -> str:
        """
        Build the complete URL with endpoint and query parameters.

        Args:
            endpoint (str): The API endpoint path
            params (Optional[Dict[str, Any]]): Query parameters

        Returns:
            str: Complete URL with parameters
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        if params:
            clean_params = {k: str(v) for k, v in params.items() if v is not None}
            if clean_params:
                url += f"?{urlencode(clean_params)}"

        return url

    def get(
        self, endpoint: str, params: dict[str, Any] | None = None, headers: dict[str, str] | None = None, **kwargs
    ) -> requests.Response:
        """
        Make a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint path
            params (Optional[Dict[str, Any]]): Query parameters
            headers (Optional[Dict[str, str]]): Additional headers for this request
            **kwargs: Additional arguments to pass to requests.get()

        Returns:
            requests.Response: The response object

        Raises:
            requests.RequestException: If the request fails
        """
        url = self._build_url(endpoint, params)

        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)

        self.logger.info(f"Sending GET request to {url}")

        return self.session.get(url, headers=request_headers, **kwargs)

    def close(self):
        """Close the session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
