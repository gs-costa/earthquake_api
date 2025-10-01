# Earthquake API - Real-time ETL Service

A real-time ETL service that ingests earthquake data from the USGS API, transforms it into relational database tables, and provides filtered query capabilities.

## Overview

This service fetches earthquake data from the [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/) on-demand when users request data, processes it through an ETL pipeline, and stores it in PostgreSQL. It provides a RESTful API for querying earthquake data by date range.

### Key Features

- **On-demand ETL**: Real-time data ingestion from USGS API triggered by user requests
- **Relational Storage**: Data stored in PostgreSQL with proper schema design
- **Date Range Queries**: Filter earthquake data by start and end times
- **Interactive Map Visualization**: Visual earthquake data with color-coded markers by magnitude
- **Audit Trail**: Tracks API requests and data processing metadata
- **Dockerized**: Easy deployment with Docker Compose

## Architecture

The service transforms USGS JSON data into two main tables:

- **`metadatas`**: Audit information (append-only)
  - API request details, URL parameters, status codes, result counts
- **`features`**: Earthquake data (upsert by event_id)
  - Foreign key relationship with metadatas table

## API Endpoints

### GET /features/

Query earthquake data within a specified date range.

**Parameters:**
- `start_time`: Start date for filtering (ISO format)
- `end_time`: End date for filtering (ISO format)

**Response:** JSON array of earthquake features

### GET /visualization/map

Get earthquake data optimized for map visualization.

**Parameters:**
- `start_time`: Start date for filtering (YYYY-MM-DD format)
- `end_time`: End date for filtering (YYYY-MM-DD format)
- `min_magnitude`: Minimum magnitude filter (default: 0.0)
- `max_magnitude`: Maximum magnitude filter (default: 10.0)

**Response:** JSON object with earthquake data optimized for mapping, including coordinates, magnitude, and metadata

### GET /visualization/map-view

Interactive HTML map visualization of earthquake data.

**Features:**
- **Color-coded markers** by magnitude:
  - 🟢 Green: 0.0-2.0 (Minor)
  - 🟢 Light Green: 2.0-4.0 (Light)
  - 🟡 Yellow: 4.0-6.0 (Moderate)
  - 🟠 Orange: 6.0-8.0 (Strong)
  - 🔴 Red: 8.0+ (Great)
- **Interactive controls** for date range and magnitude filtering
- **Detailed popups** with earthquake information
- **Real-time statistics** display
- **Responsive design** for desktop and mobile

**Response:** HTML page with interactive Leaflet.js map

## Setup

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone git@github.com:gs-costa/earthquake_api.git
cd earthquake_api
```

2. Start the service:
```bash
bash start_pipe.sh
```

This comprehensive startup script will:

**Environment Setup:**
- Check for required tools (Python 3.12+, Docker, Docker Compose)
- Create `.env` file with database configuration if it doesn't exist
- Create and activate Python virtual environment
- Install Poetry package manager
- Install all project dependencies

**Database Setup:**
- Start PostgreSQL database using Docker Compose
- Wait for database to be ready (with health checks)
- Run Alembic database migrations to create tables

**Application Launch:**
- Start the FastAPI server with auto-reload enabled
- Server available at http://localhost:8000
- Automatic cleanup on exit (Ctrl+C)

**Features:**
- Colored output for better visibility
- Error handling and validation
- Database readiness checks
- Graceful shutdown with cleanup

### Usage

Once running, access the API through:

- **API Documentation**: http://127.0.0.1:8000/docs (Swagger UI)
- **Alternative Docs**: http://127.0.0.1:8000/redoc (ReDoc)
- **Interactive Map**: http://127.0.0.1:8000/visualization/map-view
- **Postman Collection**: Import `Earthquake.postman_collection.json`

## Project Structure

```
src/
├── api/                    # API client for USGS
├── app/                    # Main application
│   ├── config/            # Configuration management
│   ├── database/          # Database models and config
│   ├── domains/           # API endpoints and schemas
│   │   ├── features/      # Earthquake data endpoints
│   │   └── visualization/ # Map visualization endpoints
│   ├── middlewares/       # Request/response middleware
│   └── repositories/      # Data access layer
└── data_integration/      # ETL pipeline components
```

## Visualization Features

The interactive map visualization provides:

- **Real-time Data**: Fetches fresh earthquake data from USGS API (limited to 20,000 results)
- **Smart Filtering**: Filter by date range and magnitude thresholds
- **Visual Indicators**: Marker size and color based on earthquake magnitude
- **Rich Information**: Click markers for detailed earthquake data including:
  - Location and coordinates
  - Magnitude and depth
  - Timestamp
  - Tsunami alerts
  - USGS alert levels
- **Error Handling**: Clear error messages for invalid date ranges or API limits
- **Responsive Design**: Works on desktop and mobile devices

