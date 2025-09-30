from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.app.database.config import SessionLocal
from src.app.middlewares.constants import ENDPOINTS_TO_BYPASS


class DatabaseSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in ENDPOINTS_TO_BYPASS:
            return await call_next(request)

        response = Response("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            request.state.db_session = SessionLocal()
            response = await call_next(request)
        finally:
            request.state.db_session.close()
        return response
