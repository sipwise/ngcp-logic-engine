"""Test ngcp-logic-engine.utils."""

from ngcp_logic_engine.utils import split_general_key

name = "user"
uuid = "3848276298220188511@atlanta.example.com:5060"


def test_single():
    """Single value should work too."""
    key = "general"
    assert split_general_key(key) == (key, None)


def test_ok():
    """Even a value with more than one ':' should work."""
    key = f"{name}:{uuid}"
    assert split_general_key(key) == (name, uuid)
