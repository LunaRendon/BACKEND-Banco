import pytest
from fastapi.testclient import TestClient

from src.utils.app import app


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as c:
        yield c