# Earthquake API - Real-time ETL Service

A real-time ETL service that ingests earthquake data from the USGS API, transforms it into relational database tables, and provides filtered query capabilities.

## Overview

This service fetches earthquake data from the [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/) on-demand when users request data, processes it through an ETL pipeline, and stores it in PostgreSQL. It provides a RESTful API for querying earthquake data by date range.

### Key Features

- **On-demand ETL**: Real-time data ingestion from USGS API triggered by user requests
- **Relational Storage**: Data stored in PostgreSQL with proper schema design
- **Date Range Queries**: Filter earthquake data by start and end times
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
- **Postman Collection**: Import `Earthquake.postman_collection.json`

## Project Structure

```
src/
├── api/                    # API client for USGS
├── app/                    # Main application
│   ├── config/            # Configuration management
│   ├── database/          # Database models and config
│   ├── domains/           # API endpoints and schemas
│   ├── middlewares/       # Request/response middleware
│   └── repositories/      # Data access layer
└── data_integration/      # ETL pipeline components
```

