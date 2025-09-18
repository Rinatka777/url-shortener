import pytest
from starlette.testclient import TestClient
from app.main import create_app


@pytest.fixture
def app():
    return create_app

@pytest.fixture
def client(app):
    return TestClient(app)


