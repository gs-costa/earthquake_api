"""
Earthquake API - A modular Python package for collecting and processing earthquake data.

This package provides:
- Base API client for making HTTP requests with configurable headers and parameters
- USGS Earthquake API client for fetching earthquake data

Modules:
- api: Base API client functionality
- clients: Specific API client implementations
"""

__version__ = "1.0.0"
__author__ = "gs-costa"

from .api import BaseAPIClient
from .clients import USGSEarthquakeClient
from .logger import Logger

__all__ = ["BaseAPIClient", "USGSEarthquakeClient", "Logger"]
