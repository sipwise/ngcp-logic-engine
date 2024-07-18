"""Module contains the RedisManager class."""

from __future__ import annotations

from redis import Redis

from ngcp_logic_engine.config import settings


class RedisManager:
    """
    Create a counter object, an abstraction of a redis key.

    Abstracts redis keys and interfaces key related operations.
    """

    central_db = Redis(
        host=settings.redis_central_host,
        port=settings.redis_central_port,
        db=settings.redis_central_db,
        decode_responses=True,
    )
    local_db = Redis(
        host=settings.redis_local_host,
        port=settings.redis_local_port,
        db=settings.redis_local_db,
        decode_responses=True,
    )

    @classmethod
    def ping_central(cls) -> None:
        """
        Ping the central Redis server.

        :raises RedisError: If the request produces an error
        """
        cls.central_db.ping()

    @classmethod
    def ping_local(cls) -> None:
        """
        Ping the local Redis server.

        :raises RedisError: If the request produces an error
        """
        cls.local_db.ping()

    @classmethod
    def increase(cls, key: str) -> int:
        """
        Increase counter value.

        Increases the current counter value by 1.
        :returns: int
        :raises RedisError: If the request produces an error
        """
        return cls.central_db.incr(key)

    @classmethod
    def create_key(cls, uuid: str, key: str) -> int:
        """
        Increase counter value.

        Increases the current counter value by 1 and updates
        it on
        :returns: int
        :raises RedisError: If the request produces an error
        """
        counter_value = cls.increase(key)
        cls.local_db.sadd(uuid, key)

        return counter_value

    @classmethod
    def decrease(cls, key: str) -> int:
        """
        Decrease counter value.

        Decreases the current counter value by 1.
        :returns: int
        :raises RedisError: If the request produces an error
        """
        value = cls.central_db.decr(key)
        if value <= 0:
            cls.central_db.delete(key)
            return 0

        return value

    @classmethod
    def get_central_value(cls, key: str) -> int:
        """
        Get the current counter value.

        Returns the integer value of the key

        :returns: The key's value.
        :rtype: int
        """
        val = cls.central_db.get(key)
        if val:
            return int(val)
        return 0

    @classmethod
    def get_local_value(cls, key: str) -> set[str]:
        """
        Get value of key in the local database.

        Returns a set containing the members of the key.

        :returns: The key's members.
        :rtype: int
        """
        val = cls.local_db.smembers(key)
        return val

    @classmethod
    def delete_key(cls, uuid: str, key: str) -> None:
        """
        Delete call-id key from local database and decrease its value.

        Removes a key for a specific dialog uuid in the local
        database and decreases its value on the
        central database.

        :return:
        """
        cls.local_db.srem(uuid, key)
        cls.decrease(key)

    @classmethod
    def _delete_local_db_dialog_id(cls, uuid: str) -> None:
        """
        Delete dialog id from local database.

        Removes the given dialog set from the local database.
        :return:
        """
        cls.local_db.delete(uuid)

    @classmethod
    def delete_dialog_id(cls, uuid: str) -> None:
        """
        Decrease keys in dialog set and remove set.

        Decreases all keys contained in the specified call-id set
        and deletes the set.
        :return:
        """
        keys = cls.local_db.smembers(uuid)
        for key in keys:
            cls.decrease(key)
        cls._delete_local_db_dialog_id(uuid)
