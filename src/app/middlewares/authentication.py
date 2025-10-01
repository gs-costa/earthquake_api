import base64

from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.app.config.config import Environment
from src.app.middlewares.constants import ENDPOINTS_TO_BYPASS


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Basic Authentication middleware for API routes.

    This middleware implements HTTP Basic Authentication using username and password.
    It checks for the Authorization header and validates credentials against
    environment variables.
    """

    def __init__(self, app, realm: str | None = None):
        super().__init__(app)
        self.realm = realm or Environment.API_REALM
        self.username = Environment.API_USERNAME
        self.password = Environment.API_PASSWORD

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in ENDPOINTS_TO_BYPASS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return self._create_unauthorized_response("Missing Authorization header")

        if not auth_header.startswith("Basic "):
            return self._create_unauthorized_response("Invalid authorization scheme")

        try:
            encoded_credentials = auth_header[6:]
            decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
            username, password = decoded_credentials.split(":", 1)
        except (ValueError, UnicodeDecodeError):
            return self._create_unauthorized_response("Invalid authorization header format")

        if username != self.username or password != self.password:
            return self._create_unauthorized_response("Invalid credentials")

        request.state.authenticated_user = username

        return await call_next(request)

    def _create_unauthorized_response(self, detail: str) -> Response:
        """
        Create a 401 Unauthorized response with WWW-Authenticate header.
        """
        from fastapi.responses import JSONResponse

        response = JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": detail})
        response.headers["WWW-Authenticate"] = f'Basic realm="{self.realm}"'
        return response
