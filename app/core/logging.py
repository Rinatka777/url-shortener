import logging
from typing import Any, Dict

import structlog


_LEVELS: Dict[str, int] = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def _to_levelno(level_name: str | int) -> int:
    if isinstance(level_name, int):
        return level_name
    if isinstance(level_name, str):
        return _LEVELS.get(level_name.upper(), logging.INFO)
    return logging.INFO


def configure_logging(service: str, env: str, level: str | int) -> None:
    level_no = _to_levelno(level)
    logging.basicConfig(
        level=level_no,
        format="%(message)s",
        force=True,
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", key="ts", utc=True),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(level_no),
        cache_logger_on_first_use=True,
    )
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(service=service, env=env)
