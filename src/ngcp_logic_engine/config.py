"""ngcp-logic-engine  settings."""

import logging
import os
from functools import lru_cache
from typing import Any

from pydantic import BaseModel


class BaseConfig(BaseModel):
    """common configs."""

    env: str = "development"
    log_level: int = logging.INFO
    env_prefix: str = "logic_engine_"
    use_dialog_id_tags: bool = False
    redis_central_host: str = "redis"
    redis_central_port: int = 6379
    redis_central_db: int = 3

    redis_local_host: str = "redis"
    redis_local_port: int = 6379
    redis_local_db: int = 4

    def __init__(self, **kwargs: Any) -> None:
        """Simulate pydantic_settings.

        at least related to environment variables.
        """
        super().__init__(**kwargs)
        # __fields__ V1 model_fields V2
        for fld in self.__fields__:
            if fld == "env_prefix":
                continue
            field = f"{self.env_prefix}{fld}"
            if field.upper() in os.environ:
                env_key = field.upper()
            elif field in os.environ:
                env_key = field
            else:
                continue
            val = os.environ[env_key]
            self.__setattr__(fld, val)


class DevelopmentConfig(BaseConfig):
    """development config."""

    log_level: int = logging.DEBUG


class ProductionConfig(BaseConfig):
    """production config."""


class TestingConfig(BaseConfig):
    """configs for testing."""

    log_level: int = logging.DEBUG
    redis_central_host: str = "localhost"
    redis_local_host: str = "localhost"


@lru_cache
def get_settings() -> BaseConfig:
    """Return settings depending on the environment."""
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    base_conf = BaseConfig()
    config_cls = config_cls_dict[base_conf.env]
    return config_cls()


settings = get_settings()
