"""Module contains the Counter class."""

from __future__ import annotations

from redis import Redis

from ngcp_logic_engine.config import settings


class Counter:
    """
    Create a counter object, an abstraction of a redis key.

    Abstracts redis keys and interfaces key related operations.
    The combinations of parameters "name:uuid" represents a redis key.

    :param name: right-hand side parameter of the redis key
    :param uuid: left-hand side parameter of the redis key
    """

    @classmethod
    def ping(cls) -> None:
        """Ping the Redis server.

        :raises RedisError: If the request produces an error
        """
        cls.redis_db.ping()

    def __init__(self, name: str, uuid: str | None = None, redis: Redis[bytes] | None = None):
        self.key: str = self.generate_key(name, uuid)
        if redis:
            self.redis_db = redis
        else:
            self.redis_db = Redis(
                host=settings.redis_host, port=settings.redis_port, db=settings.redis_db
            )

    @classmethod
    def generate_key(cls, name: str, uuid: str | None = None) -> str:
        """
        Generate counter key.

        Creates a redis key from the class' name and uuid parameters. If no uuid
        parameter is passed (i.e. a name member of the GeneralCounter Enum) then
        the key is set to the name.
        :returns: The redis key
        :rtype: str
        """
        if uuid is None:
            return f"{name}"
        return f"{name}:{uuid}"

    def increase(self) -> int:
        """
        Increase counter value.

        Increases the current counter value by 1 and updates
        it on
        :returns: int
        :raises RedisError: If the request produces an error
        """
        return self.redis_db.incr(self.key)

    def decrease(self) -> int:
        """
        Decrease counter value.

        Decreases the current counter value by 1.
        :returns: int
        :raises RedisError: If the request produces an error
        """
        return self.redis_db.decr(self.key)

    def value(self) -> int:
        """
        Get the current counter value.

        This method is a public interface that wraps the private method `_get_counter_value`.

        :returns: The counter's value.
        :rtype: int
        """
        val = self.redis_db.get(self.key)
        if val:
            return int(val)
        return 0
