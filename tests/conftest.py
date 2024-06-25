"""settings for pytest."""

import pytest

from ngcp_logic_engine import config


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
