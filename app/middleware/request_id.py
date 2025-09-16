import uuid
import time
import typing
import structlog
import fastapi


REQUEST_ID_HEADER = "x-request-id"

def generate_request_id() -> str:
    id = uuid.uuid4()
    return f"{id}"

def get_request_id(request) -> str:
