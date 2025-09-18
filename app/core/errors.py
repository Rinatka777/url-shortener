from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


def _error_response(rid: str, status: int, type_: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        headers={"X-Request-ID": rid},
        content={"error": {"type": type_, "message": message, "request_id": rid}},
    )


async def http_exception_handler(request, exc):
    rid = getattr(request.state, "request_id", "unknown")
    message = getattr(exc, "detail", "HTTP error")
    return _error_response(rid, getattr(exc, "status_code", 500), "http_error", str(message))


async def validation_exception_handler(request, exc: RequestValidationError):
    rid = getattr(request.state, "request_id", "unknown")
    return _error_response(rid, 422, "validation_error", "Invalid request")


async def unhandled_exception_handler(request, exc):
    rid = getattr(request.state, "request_id", "unknown")
    return _error_response(rid, 500, "internal_error", "Internal server error")


def init_error_handlers(app):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
