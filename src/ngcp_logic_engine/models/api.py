"""BaseModel definitions."""

from enum import Enum, EnumMeta

from pydantic import BaseModel


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


class MetaEnum(EnumMeta):
    """Overload the __contains__ magic method."""

    def __contains__(self, item: object) -> bool:
        """Check if 'item' is a valid member of the Enum."""
        if not isinstance(item, str):
            return False
        try:
            self(item)
        except ValueError:
            return False
        else:
            return True


class BaseEnum(Enum, metaclass=MetaEnum):
    """Expands Enum class with MetaEnum as metaclass."""

    @classmethod
    def list(cls) -> list[str]:
        """Dump Enum member values as a list."""
        return [element.value for element in cls]


class CallCounter(str, BaseEnum):
    """Contains all counters tied to an identification number."""

    user = "user"
    userout = "userout"
    totaluser = "totaluser"
    totaluserout = "totaluserout"
    account = "account"
    accountout = "accountout"
    totalaccount = "totalaccount"
    totalaccountout = "totalaccountout"
    location = "location"
    totallocation = "totallocation"
    peer = "peer"
    peerout = "peerout"


class GeneralCounter(str, BaseEnum):
    """Contains all counters that are independent of an identification number."""

    local = "local"
    total = "total"
    incoming = "incoming"
    outgoing = "outgoing"
    relay = "relay"
    emergency = "emergency"
    peer_voicebox = "peer:voicebox"
    peer_faxserver = "peer:faxserver"
    peer_appsrv = "peer:appsrv"
    peer_pbxsrv = "peer:pbxsrv"


class CounterResult(BaseModel):
    """Result of getter."""

    name: str
    value: int
