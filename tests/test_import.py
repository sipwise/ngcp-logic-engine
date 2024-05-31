"""Test ngcp-logic-engine."""

import ngcp_logic_engine


def test_import() -> None:
    """Test that the app can be imported."""
    assert isinstance(ngcp_logic_engine.__name__, str)
