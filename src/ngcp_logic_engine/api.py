"""ngcp-logic-engine REST API."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated
from urllib.request import Request

import coloredlogs
from fastapi import APIRouter, Body, FastAPI, status
from redis import RedisError
from starlette.responses import JSONResponse

from ngcp_logic_engine import config
from ngcp_logic_engine.dialogmanager import DialogManager
from ngcp_logic_engine.models.api import CounterResult, HealthCheck
from ngcp_logic_engine.models.dialog import (
    AccountDialogIdBundle,
    ActiveUserDialogParams,
    CalleeDialogIdBundle,
    CalleeDialogParams,
    CallerDialogIdBundle,
    CallerDialogParams,
    CounterDialogParams,
    DialogBundle,
    HuntgroupDialogIdBundle,
    LocationDialogIdBundle,
    PeerDialogIdBundle,
    PeerDialogParams,
    ResellerDialogIdBundle,
    UserDialogIdBundle,
)
from ngcp_logic_engine.openapi import examples
from ngcp_logic_engine.redismanager import RedisManager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle FastAPI startup and shutdown events."""
    # Startup events:
    # - Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # - Add coloredlogs' colored StreamHandler to the root logger.
    coloredlogs.install(level=config.settings.log_level)
    yield
    # Shutdown events.


api_v1 = APIRouter(prefix="/api/v1/dialog")
app = FastAPI(lifespan=lifespan)


@app.exception_handler(ValueError)
async def value_error_exception_handler(
    request: Request, exc: ValueError
) -> JSONResponse:
    """Map value errors to HTTPRequestError with code 400."""
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.get(
    "/health",
    tags=["Health Check"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
def get_health() -> HealthCheck:
    """Perform a Health Check.

    Endpoint to perform a healthcheck on. This endpoint can primarily be used
    by Docker to ensure a robust container orchestration and management is in
    place. Other services which rely on proper functioning of the API service
    will not deploy if this endpoint returns any other HTTP status code except
    200 (OK).

    :returns: HealthCheck: A JSON response with the health status.
    """
    return HealthCheck(status="OK")


@app.get(
    "/ping",
    tags=["Redis"],
    summary="Verify that redis connection is alive.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
def ping_redis() -> bool:
    """Check redis connection.

    Verifies that the application is correctly connected to redis.
    :returns: True if the connection was successful and False otherwise
    :rtype: bool
    """
    try:
        RedisManager.ping_central()
        RedisManager.ping_local()
    except RedisError:
        return False
    else:
        return True


@app.get(
    "/api/v1/counter/{key}",
    tags=["Counter Getter"],
    summary="Get the value of a counter.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
def get_counter(key: str) -> CounterResult:
    """Get the value of a counter.

    :returns: Value of the counter
    :rtype: CounterResult
    """
    return CounterResult(name=key, value=RedisManager.get_central_value(key))


@api_v1.post(
    "/counter",
    tags=["Counter Adders"],
    summary="Increase a dialog's counters related to a the specified key.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def initialize_counter_dialog_profile(
    params: Annotated[
        CounterDialogParams,
        Body(openapi_examples=examples.routes.post.counter.payload),
    ],
) -> None:
    """
    Set up a new dialog profile for the specified counter.

    Creates a new profile for the dialog and updates the specified counter.
    :param params:
    :return:
    """
    DialogManager.set_dialog_profile_counter(params)


@api_v1.post(
    "/peer",
    tags=["Counter Adders"],
    summary="Increase a dialog's counters related to a peer",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def initialize_peer_dialog_profile(
    params: Annotated[
        PeerDialogParams,
        Body(openapi_examples=examples.routes.post.peer.payload),
    ],
) -> None:
    """
    Set up a new dialog profile for a peer.

    Creates a new profile for the dialog and updates all the relevant counters
    for the peer.
    :param params:
    :return:
    """
    DialogManager.set_dialog_profile_peer(params)


@api_v1.post(
    "/user/caller",
    tags=["Counter Adders"],
    summary="Increase a dialog's counters related to a caller",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def initialize_caller_dialog_profile(
    params: Annotated[
        CallerDialogParams,
        Body(openapi_examples=examples.routes.post.caller.payload),
    ],
) -> None:
    """
    Set up a new dialog profile for a caller.

    Creates a new profile for the dialog and updates all the relevant counters
    for the caller.
    :param params:
    :return:
    """
    DialogManager.set_dialog_profile_caller(params)


@api_v1.post(
    "/user/callee",
    tags=["Counter Adders"],
    summary="Increase a dialog's counters related to a callee",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def initialize_callee_dialog_profile(
    params: Annotated[
        CalleeDialogParams,
        Body(openapi_examples=examples.routes.post.callee.payload),
    ],
) -> None:
    """
    Set up a new dialog profile for a callee.

    Creates a new profile for the dialog and updates all the relevant counters
    for the callee.
    :param params:
    :return:
    """
    DialogManager.set_dialog_profile_callee(params)


@api_v1.post(
    "/user/caller/active",
    tags=["Counter Adders"],
    summary="Increase a dialog's counters related to an active caller",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def initialize_active_caller_dialog_profile(
    params: Annotated[
        ActiveUserDialogParams,
        Body(openapi_examples=examples.routes.post.activeuser.payload),
    ],
) -> None:
    """
    Set up a new dialog profile for an active caller.

    Creates a new profile for the dialog and updates all the relevant counters
    for the active caller.
    :param params:
    :return:
    """
    DialogManager.set_dialog_profile_caller_active(params)


@api_v1.post(
    "/user/callee/active",
    tags=["Counter Adders"],
    summary="Increase a dialog's counters related to an active callee",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def initialize_active_callee_dialog_profile(
    params: Annotated[
        ActiveUserDialogParams,
        Body(openapi_examples=examples.routes.post.activeuser.payload),
    ],
) -> None:
    """
    Set up a new dialog profile for an active callee.

    Creates a new profile for the dialog and updates all the relevant counters
    for the active callee.
    :param params:
    :return:
    """
    DialogManager.set_dialog_profile_callee_active(params)


@api_v1.post(
    "/user/caller/totals",
    tags=["Counter Adders"],
    summary="Increase a dialog's total counters related to a caller",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def initialize_caller_totals_dialog_profile(
    params: Annotated[
        CallerDialogParams,
        Body(openapi_examples=examples.routes.post.caller.payload),
    ],
) -> None:
    """
    Set up a new dialog profile for a caller, inclusive of totals.

    Creates a new profile for the dialog and updates all the relevant counters
    for the caller, including totals.
    :param params:
    :return:
    """
    DialogManager.set_dialog_profile_caller_totals(params)


@api_v1.post(
    "/user/callee/totals",
    tags=["Counter Adders"],
    summary="Increase a dialog's total counters related to a callee",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def initialize_callee_totals_dialog_profile(
    params: Annotated[
        CalleeDialogParams,
        Body(openapi_examples=examples.routes.post.callee.payload),
    ],
) -> None:
    """
    Set up a new dialog profile for a callee, inclusive of totals.

    Creates a new profile for the dialog and updates all the relevant counters
    for the callee, including totals.
    :param params:
    :return:
    """
    DialogManager.set_dialog_profile_callee_totals(params)


@api_v1.put(
    "/delete",
    tags=["Counter Purge"],
    summary="Delete a dialog.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def delete_dialog_profile(
    bundle: Annotated[
        DialogBundle, Body(openapi_examples=examples.routes.put.delete.payload)
    ],
) -> None:
    """
    Remove dialog record from database for a dialog.

    Deletes the dialog from the local database.
    :param dialog: Dialog object containing the id parameters of the dialog.
    :return:
    """
    DialogManager.delete_dialog_profile(bundle.dialog)


@api_v1.put(
    "/delete/user",
    tags=["Counter Subtractors"],
    summary="Decrease a dialog's counters with a specific user id.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def delete_user_dialog_profile(
    bundle: Annotated[
        UserDialogIdBundle,
        Body(openapi_examples=examples.routes.put.user.payload),
    ],
) -> None:
    """
    Update counter values and remove dialog record from database for a user.

    Decreases counter values for the user profile and deletes the dialog
    from the local database.
    :param bundle:
    :return:
    """
    DialogManager.delete_dialog_profile_user(bundle)


@api_v1.put(
    "/delete/account",
    tags=["Counter Subtractors"],
    summary="Decrease a dialog's counters with a specific account id.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def delete_account_dialog_profile(
    bundle: Annotated[
        AccountDialogIdBundle,
        Body(openapi_examples=examples.routes.put.account.payload),
    ],
) -> None:
    """
    Update counter values and remove dialog record from database for an
    account.

    Decreases counter values for the account profile and deletes the dialog
    from the local database.
    :param bundle:
    :return:
    """
    DialogManager.delete_dialog_profile_account(bundle)


@api_v1.put(
    "/delete/reseller",
    tags=["Counter Subtractors"],
    summary="Decrease a dialog's counters with a specific reseller id.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def delete_reseller_dialog_profile(
    bundle: Annotated[
        ResellerDialogIdBundle,
        Body(openapi_examples=examples.routes.put.reseller.payload),
    ],
) -> None:
    """
    Update counter values and remove dialog record from database for a
    reseller.

    Decreases counter values for the reseller profile and deletes the dialog
    from the local database.
    :param bundle:
    :return:
    """
    DialogManager.delete_dialog_profile_reseller(bundle)


@api_v1.put(
    "/delete/location",
    tags=["Counter Subtractors"],
    summary="Decrease a dialog's counters with a specific location id.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def delete_location_dialog_profile(
    bundle: Annotated[
        LocationDialogIdBundle,
        Body(openapi_examples=examples.routes.put.location.payload),
    ],
) -> None:
    """
    Update counter values and remove dialog record from database for a
    location.

    Decreases counter values for the location profile and deletes the dialog
    from the local database.
    :param bundle:
    :return:
    """
    DialogManager.delete_dialog_profile_location(bundle)


@api_v1.put(
    "/delete/peer",
    tags=["Counter Subtractors"],
    summary="Decrease a dialog's counters with a specific peer id.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def delete_peer_dialog_profile(
    bundle: Annotated[
        PeerDialogIdBundle,
        Body(openapi_examples=examples.routes.put.peer.payload),
    ],
) -> None:
    """
    Update counter values and remove dialog record from database for a peer.

    Decreases counter values for the peer profile and deletes the dialog
    from the local database.
    :param bundle:
    :return:
    """
    DialogManager.delete_dialog_profile_peer(bundle)


@api_v1.put(
    "/delete/user/active",
    tags=["Counter Subtractors"],
    summary="Decrease a dialog's counters related to an active user.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def delete_active_user_dialog_profile(
    bundle: Annotated[
        UserDialogIdBundle,
        Body(openapi_examples=examples.routes.put.user.payload),
    ],
) -> None:
    """
    Update counter values and remove dialog record from database for a user.

    Decreases counter values for the user profile and deletes the dialog
    from the local database.
    :param bundle:
    :return:
    """
    DialogManager.delete_dialog_profile_active_user(bundle)


@api_v1.put(
    "/delete/transferred/callee",
    tags=["Counter Subtractors"],
    summary="Decrease a dialog's counters related to an transferred callee.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def delete_transferred_callee_dialog_profile(
    bundle: Annotated[
        CalleeDialogIdBundle,
        Body(openapi_examples=examples.routes.put.callee.payload),
    ],
) -> None:
    """
    Update counter values and remove dialog record from database for a
    transferred callee.

    Decreases counter values for the transferred callee profile and deletes
    the dialog from the local database.
    :param bundle:
    :return:
    """
    DialogManager.delete_dialog_profile_transferred_callee(bundle)


@api_v1.put(
    "/delete/transferred/caller",
    tags=["Counter Subtractors"],
    summary="Decrease a dialog's counters related to an transferred caller.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def delete_transferred_caller_dialog_profile(
    bundle: Annotated[
        CallerDialogIdBundle,
        Body(openapi_examples=examples.routes.put.caller.payload),
    ],
) -> None:
    """
    Update counter values and remove dialog record from database for a
    transferred caller.

    Decreases counter values for the transferred caller profile and deletes
    the dialog from the local database.
    :param bundle:
    :return:
    """
    DialogManager.delete_dialog_profile_transferred_caller(bundle)


@api_v1.put(
    "/delete/huntgroup",
    tags=["Counter Subtractors"],
    summary="Decrease a dialog's counters related to a huntgroup.",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
async def delete_huntgroup_member_dialog_profile(
    bundle: Annotated[
        HuntgroupDialogIdBundle,
        Body(openapi_examples=examples.routes.put.huntgroup.payload),
    ],
) -> None:
    """
    Update counter values and remove dialog record from database for a
    huntgroup member.

    Decreases counter values for the huntgroup member profile and deletes the
    dialog from the local database.
    :param bundle:
    :return:
    """
    DialogManager.delete_dialog_profile_huntgroup_member(bundle)


app.include_router(api_v1)
