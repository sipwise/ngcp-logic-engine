"""Module contains the RedisManager class."""

from __future__ import annotations

import logging

from redis import Redis

from ngcp_logic_engine.config import settings

logger = logging.getLogger(__name__)


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
        res = cls.central_db.incr(key)
        logger.debug("%s increased to %d", key, res)
        return res

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
        cls.local_db.lpush(uuid, key)
        logger.debug("%s added to uuid:%s", key, uuid)
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
            logger.debug("%s was <= 0, removed", key)
            return 0
        logger.debug("%s descreased to %d", key, value)
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
    def get_local_value(cls, key: str) -> list[str]:
        """
        Get value of key in the local database.

        Returns a list containing the members of the key.

        :returns: The key's members.
        :rtype: int
        """
        val = cls.local_db.lrange(key, 0, -1)
        return val

    @classmethod
    def delete_key(cls, uuid: str, key: str) -> None:
        """
        Delete call-id key from local database and decrease its value from the
        central database.

        Removes a key for a specific dialog uuid in the local
        database and decreases its value on the
        central database. If no key is found on the local database
        the central database is deletion operation is skipped.

        :return:
        """
        val = cls.local_db.lrem(uuid, 1, key)
        logger.debug("%s deleted from uuid:%s", key, uuid)
        if val > 0:
            cls.decrease(key)

    @classmethod
    def _delete_local_db_dialog_id(cls, uuid: str) -> None:
        """
        Delete dialog id from local database.

        Removes the given dialog list from the local database.
        :return:
        """
        cls.local_db.delete(uuid)
        logger.debug("%s deleted", uuid)

    @classmethod
    def delete_dialog_id(cls, uuid: str) -> None:
        """
        Decrease keys in dialog set and remove set.

        Decreases all keys contained in the specified call-id set
        and deletes the set.
        :return:
        """
        keys = cls.local_db.lrange(uuid, 0, -1)
        logger.debug("%s decreasing keys", uuid)
        for key in keys:
            cls.decrease(key)
        cls._delete_local_db_dialog_id(uuid)
