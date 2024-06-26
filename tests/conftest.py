"""settings for pytest."""

import pytest

from ngcp_logic_engine import config
from ngcp_logic_engine.api import Counter


def pytest_configure(config):
    """Define markers."""
    config.addinivalue_line("markers", "nomockenv")


@pytest.fixture(autouse=True)
def mock_env_testing(request, monkeypatch):
    """Force testing environment."""
    if "nomockenv" in request.keywords:
        return config.settings
    monkeypatch.setenv("LOGIC_ENGINE_ENV", "testing")
    monkeypatch.setattr(config, "settings", config.TestingConfig())

    settings = config.settings
    assert settings.env == "testing"
    return settings


@pytest.fixture()
def redis_client():
    """Provide a fake redis connection."""
    import fakeredis

    redis_client = fakeredis.FakeRedis()
    return redis_client


@pytest.fixture()
def fake_counters(redis_client, monkeypatch, request):
    """Provide counter with fake redis connection."""

    def counter(name, uuid=None):
        cnt = Counter(name, uuid)
        cnt.redis_db = redis_client
        return cnt

    monkeypatch.setattr("ngcp_logic_engine.api.Counter", counter)
    return redis_client
