"""ngcp-logic-engine REST API."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import coloredlogs
from fastapi import FastAPI, status
from redis import RedisError

from ngcp_logic_engine.counters import Counter
from ngcp_logic_engine.models.api import HealthCheck
from ngcp_logic_engine.utils import (
    check_valid_counter,
    check_valid_general_counter,
    split_general_key,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle FastAPI startup and shutdown events."""
    # Startup events:
    # - Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # - Add coloredlogs' colored StreamHandler to the root logger.
    coloredlogs.install()
    yield
    # Shutdown events.


app = FastAPI(lifespan=lifespan)


@app.get(
    "/api/v1/counter/{name}",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def get_general_counter(name: str) -> int:
    """Get value of general counter.

    Retrieves the value of the specified counter.
    :param name: counter name
    :returns: The counter's value
    :rtype: int
    """
    check_valid_general_counter(name)
    counter = Counter(*split_general_key(name))
    return counter.value()


@app.get(
    "/api/v1/counter/{name}/{uuid}",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def get_counter(name: str, uuid: str) -> int:
    """Get value of counter.

    Retrieves the value of the specified counter.
    :param name: counter name
    :param uuid: counter id
    :returns: The counter's value
    :rtype: int
    """
    check_valid_counter(name)
    counter = Counter(name, uuid)
    return counter.value()


@app.post(
    "/api/v1/counter/increase/{name}/{uuid}",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def increase_counter(name: str, uuid: str) -> int | None:
    """Increase the value of the specified counter.

    Increases the value of the specified counter by one.
    :param name: counter name
    :param uuid: counter id
    :returns: OK
    :rtype: str
    """
    check_valid_counter(name)
    counter = Counter(name, uuid)
    new_counter_value = counter.increase()
    return new_counter_value


@app.post(
    "/api/v1/counter/decrease/{name}/{uuid}",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def decrease_counter(name: str, uuid: str) -> int | None:
    """Decrease the value of the specified counter.

    Decreases the value of the specified counter by 1.
    :param name: counter name
    :param uuid: counter id
    :returns: OK
    :rtype: str
    """
    check_valid_counter(name)
    counter = Counter(name, uuid)
    new_counter_value = counter.decrease()
    return new_counter_value


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
def get_health() -> HealthCheck:
    """Perform a Health Check.

    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).

    Returns
    -------
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


@app.get(
    "/ping",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
def ping_redis() -> bool:
    """Check redis connection.

    Verifies that the application is correctly connected to redis.
    :returns: true if the connection was successful and false otherwise
    :rtype: bool
    """
    try:
        Counter.ping()
    except RedisError:
        return False
    else:
        return True
