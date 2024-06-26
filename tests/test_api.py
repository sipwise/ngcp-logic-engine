"""Test ngcp-logic-engine REST API."""

import httpx
from fastapi.testclient import TestClient

from ngcp_logic_engine.api import app
from ngcp_logic_engine.models.api import HealthCheck

client = TestClient(app)
mock_uuid = "3848276298220188511@atlanta.example.com"
init_val = 17


def test_health() -> None:
    """Test the health endpoint returns a successful response."""
    response = client.get("/health")
    assert response.status_code == httpx.codes.OK
    assert response.json() == HealthCheck(status="OK").model_dump()


def test_get_general_counter_success(fake_counters) -> None:
    """Test getting a general counter successfully."""
    response = client.get("/api/v1/counter/local")
    assert response.status_code == httpx.codes.OK
    assert isinstance(response.json(), int)
    assert response.json() == 0


def test_get_general_counter_invalid() -> None:
    """Test getting a general counter with an invalid name returns an error."""
    response = client.get("/api/v1/counter/fakename")
    assert response.status_code == httpx.codes.BAD_REQUEST


def test_get_counter_success(fake_counters) -> None:
    """Test getting a specific counter successfully."""
    fake_counters.set(f"user:{mock_uuid}", init_val)
    response = client.get(f"/api/v1/counter/user/{mock_uuid}")
    assert response.status_code == httpx.codes.OK
    assert isinstance(response.json(), int)
    assert response.json() == init_val


def test_get_counter_without_uuid_invalid() -> None:
    """Test getting a counter with an invalid name returns an error."""
    response = client.get("/api/v1/counter/user")
    assert response.status_code == httpx.codes.BAD_REQUEST


def test_get_counter_invalid() -> None:
    """Test getting a counter with an invalid name returns an error."""
    response = client.get(f"/api/v1/counter/fake/{mock_uuid}")
    assert response.status_code == httpx.codes.BAD_REQUEST


def test_increase_counter(fake_counters):
    """Test increasing a counter with a valid name."""
    fake_counters.set(f"user:{mock_uuid}", init_val)
    response = client.post(f"/api/v1/counter/increase/user/{mock_uuid}")
    assert response.status_code == httpx.codes.OK
    assert isinstance(response.json(), int)
    assert response.json() == init_val + 1


def test_increase_counter_invalid() -> None:
    """Test increasing a counter with an invalid name returns an error."""
    response = client.post(f"/api/v1/counter/increase/fake/{mock_uuid}")
    assert response.status_code == httpx.codes.BAD_REQUEST


def test_decrease_counter(fake_counters) -> None:
    """Test decreasing a counter with a valid name."""
    fake_counters.set(f"user:{mock_uuid}", init_val)
    response = client.post(f"/api/v1/counter/decrease/user/{mock_uuid}")
    assert response.status_code == httpx.codes.OK
    assert isinstance(response.json(), int)
    assert response.json() == init_val - 1


def test_decrease_counter_invalid() -> None:
    """Test increasing a counter with an invalid name returns an error."""
    response = client.post(f"/api/v1/counter/decrease/fake/{mock_uuid}")
    assert response.status_code == httpx.codes.BAD_REQUEST
