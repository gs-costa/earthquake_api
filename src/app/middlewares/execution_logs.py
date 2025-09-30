import time

from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.app.database.models import ExecutionLogs
from src.app.middlewares.constants import ENDPOINTS_TO_BYPASS
from src.app.repositories.database_repository import DatabaseRepository
from src.logger import Logger


class ExecutionLogsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        logger = Logger(__name__)
        start_time = time.time()
        response: Response = await call_next(request)
        execution_time = time.time() - start_time
        if request.url.path not in ENDPOINTS_TO_BYPASS:
            db: Session = request.state.db_session
            data = ExecutionLogs(
                endpoint_name=request.url.path,
                execution_time=round(execution_time, 2),
                status_code=int(response.status_code),
                parameters=dict(request.query_params),
            )

            repository = DatabaseRepository(model=ExecutionLogs, session=db)
            try:
                repository.create(data)
            except Exception as e:
                logger.error(f"Failed to log execution data: {e}")
                raise e

        return response
