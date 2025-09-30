from fastapi import FastAPI, responses
from fastapi.middleware.cors import CORSMiddleware

from src.app.domains.features.endpoints import features_router
from src.app.middlewares.database_session import DatabaseSessionMiddleware
from src.app.middlewares.execution_logs import ExecutionLogsMiddleware

app = FastAPI(
    title="Earthquake API ETL Service",
    redoc_url="/redoc",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.include_router(features_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
app.add_middleware(DatabaseSessionMiddleware)
app.add_middleware(ExecutionLogsMiddleware)


@app.get("/", include_in_schema=False)
def read_root():
    return responses.RedirectResponse(url="/docs")
