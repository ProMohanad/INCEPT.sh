"""X-Request-ID propagation middleware."""

from __future__ import annotations

import re
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

# Only accept UUIDs or safe alphanumeric+dash IDs (max 128 chars)
_VALID_REQUEST_ID = re.compile(r"^[a-zA-Z0-9\-_]{1,128}$")


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Generate or propagate X-Request-ID header."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_id = request.headers.get("X-Request-ID", "")
        if client_id and _VALID_REQUEST_ID.match(client_id):
            request_id = client_id
        else:
            request_id = str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
