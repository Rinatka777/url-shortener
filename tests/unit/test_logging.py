import json
import structlog

from app.core.logging import configure_logging


def _last_json_from_stderr(capsys):
    captured = capsys.readouterr()
    data = captured.err.strip().splitlines()
    return json.loads(data[-1]) if data else None


def test_configure_logging_emits_structured_json_with_service_env_and_level(capsys):
    configure_logging(service="url-shortener", env="dev", level="INFO")
    log = structlog.get_logger()
    log.info(
        "http_request",
        request_id="test-rid",
        method="GET",
        path="/health",
        status=200,
        duration_ms=3,
    )
    obj = _last_json_from_stderr(capsys)
    assert obj is not None
    assert obj["event"] == "http_request"
    assert obj["level"] == "info" or obj["level"] == "INFO"
    assert "ts" in obj and isinstance(obj["ts"], str) and "T" in obj["ts"]
    assert obj["service"] == "url-shortener"
    assert obj["env"] == "dev"
    assert obj["request_id"] == "test-rid"
    assert obj["method"] == "GET"
    assert obj["path"] == "/health"
    assert obj["status"] == 200
    assert obj["duration_ms"] == 3


def test_level_filtering_respects_threshold(capsys):
    configure_logging(service="url-shortener", env="dev", level="ERROR")
    log = structlog.get_logger()
    log.info("will_not_show")
    nothing = capsys.readouterr()
    assert not nothing.err.strip().splitlines()
    log.error("will_show", foo="bar")
    obj = _last_json_from_stderr(capsys)
    assert obj["event"] == "will_show"
    assert obj["level"] in ("error", "ERROR")
    assert obj["service"] == "url-shortener"
    assert obj["env"] == "dev"
    assert obj["foo"] == "bar"
