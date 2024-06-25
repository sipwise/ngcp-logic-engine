"""Test ngcp-logic-engine settings."""

import pytest

from ngcp_logic_engine import config


@pytest.mark.nomockenv()
def test_default_env():
    """Default env is development."""
    assert isinstance(config.settings, config.DevelopmentConfig)
    assert config.settings.env == "development"


def test_env_for_tests():
    """Default environment for tests is testing."""
    assert isinstance(config.settings, config.TestingConfig)
