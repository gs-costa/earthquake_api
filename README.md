# Earthquake API real-time ETL Service

Ingestion data from open API https://earthquake.usgs.gov/fdsnws/event/1/
Transform its json in 2 relationals tables: metadatas and features (have a foreign key, metadata_id, with metadatas)
Store data in Postgres database hosted by Docker, it's schemas are in folder src/app/database/models. Features upsert data, metadatas append only.
Metadatas table has when the API request was generated, url with params used, status code, results count for audit trail.
Provided endpoint /features/ which accepts start_time and end_time as params
Table execution_logs have informations about requests in endpoint /features/

## Project organization

-- add project tree

## How it works

1. Endpoint /features/ is requested, it calls real-time ETL of data provided by USGS Earthquake API.
    - ingest JSON format data
    - transform to sql table
    - load metada (append only) and features (upsert by event_id) to PostgreSQL database
2. App filter in PostgreSQL table features for dates between start_time and end_time, which user provided in params.
3. Load request informations in execution_logs table.
4. User receive data filtered in format application/json.

## Setup

### Pre-requisites

- Git
- Python ^3.12
- Docker

### MacOS commands

Clone repository to your local machine

```
git clone git@github.com:gs-costa/earthquake_api.git
```

Open terminal, with Docker running, type the following code:

```
bash start_pipe.sh
```
This command will run a script that will activate

### Use API

Import collection `Earthquake.postman_collection.json` to your Postman app or
visit http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc to access documentation.

