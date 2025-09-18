import time
import uuid

import fastapi
import structlog
from starlette.middleware.base import BaseHTTPMiddleware


REQUEST_ID_HEADER = "X-Request-ID"


def generate_request_id() -> str:
    return uuid.uuid4().hex


def get_request_id(request) -> str:
    rid = request.headers.get(REQUEST_ID_HEADER)
    if rid and rid.strip():
        return rid
    rid = request.headers.get(REQUEST_ID_HEADER.lower())
    if rid and rid.strip():
        return rid
    return generate_request_id()


def now_ms() -> float:
    return time.perf_counter() * 1000.0


class RequestIDMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: fastapi.FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request, call_next):
        t0 = now_ms()
        rid = get_request_id(request)
        request.state.request_id = rid
        method = request.method
        path = request.url.path

        structlog.contextvars.bind_contextvars(request_id=rid, method=method, path=path)
        log = structlog.get_logger()

        response = None
        try:
            response = await call_next(request)
            status = response.status_code
        except Exception:
            duration_ms = int(now_ms() - t0)
            log.exception(
                "http_request_error",
                request_id=rid,
                method=method,
                path=path,
                duration_ms=duration_ms,
            )
            raise
        else:
            duration_ms = int(now_ms() - t0)
            response.headers[REQUEST_ID_HEADER] = rid
            log.info(
                "http_request",
                request_id=rid,
                method=method,
                path=path,
                status=status,
                duration_ms=duration_ms,
            )
            return response
        finally:
            try:
                structlog.contextvars.unbind_contextvars("request_id", "method", "path")
            except Exception:
                pass
