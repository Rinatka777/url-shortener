import pytest
from starlette.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_generates_request_id_and_sets_header(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert "x-request-id" in r.headers
    assert r.headers["x-request-id"]


def test_propagates_incoming_request_id(client):
    rid = "test-123"
    r = client.get("/health", headers={"x-request-id": rid})
    assert r.status_code == 200
    assert r.headers["x-request-id"] == rid
