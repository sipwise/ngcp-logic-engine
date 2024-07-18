"""settings for pytest."""

import pytest

from ngcp_logic_engine import config
from ngcp_logic_engine.api import DialogManager, RedisManager


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
def redis_client_central():
    """Provide a fake redis connection."""
    import fakeredis

    redis_client_central_db = fakeredis.FakeRedis(decode_responses=True)
    return redis_client_central_db


@pytest.fixture()
def redis_client_local():
    """Provide a fake redis connection."""
    import fakeredis

    redis_client_local_db = fakeredis.FakeRedis(decode_responses=True)
    return redis_client_local_db


@pytest.fixture()
def fake_redis_manager(redis_client_central, redis_client_local, monkeypatch):
    """Provide a mock RedisManager object."""
    RedisManager.central_db = redis_client_central
    RedisManager.local_db = redis_client_local

    return RedisManager


@pytest.fixture()
def fake_dialog_manager(fake_redis_manager, monkeypatch):
    """Provide a mock DialogManager object."""
    return DialogManager
