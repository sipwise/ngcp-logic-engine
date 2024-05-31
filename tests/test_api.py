"""Test ngcp-logic-engine REST API."""

import httpx
from fastapi.testclient import TestClient

from ngcp_logic_engine.api import app

client = TestClient(app)


def test_health() -> None:
    """Test health is successful."""
    response = client.get("/health")
    assert httpx.codes.is_success(response.status_code)
