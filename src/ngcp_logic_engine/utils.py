"""Module contains utility methods used thought the applications."""

from fastapi import HTTPException

from ngcp_logic_engine.models.api import CallCounter, GeneralCounter


def check_valid_call_counter(name: str) -> None:
    """Check if counter is valid.

    Verifies that the given name is a member of the Counter enum.
    On the contrary, an HTTPException will be raised
    :param name: Counter name
    :raises HTTPException: 400 - Invalid counter
    :returns: None
    """
    if name not in CallCounter:
        raise HTTPException(status_code=400, detail="Invalid counter")


def check_valid_general_counter(name: str) -> None:
    """Check if counter is valid.

    Verifies that the given name is a member of the GeneralCounter enum.
    On the contrary, an HTTPException will be raised.
    :param name: Counter name
    :raises HTTPException: 400 - Invalid counter
    :returns: None
    """
    if name not in GeneralCounter:
        raise HTTPException(status_code=400, detail="Invalid counter")


def split_general_key(key: str) -> tuple[str, str | None]:
    """Split the values of a general counter.

    Separates the colon delimited values of a general counter into its
    name and type.
    :param key: str General counter key
    :returns: A list containing the constituents of the general counter key
    :rtype: (name, uuid)
    """
    try:
        name, uuid = key.split(":", 1)
    except ValueError:
        return (key, None)
    else:
        return (name, uuid)
