"""ngcp-logic-engine  settings."""

import logging
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """common configs."""

    env: str = "development"
    log_level: int = logging.INFO
    model_config = SettingsConfigDict(env_prefix="logic_engine_")
    use_dialog_id_tags: bool = False
    redis_central_host: str = "redis"
    redis_central_port: int = 6379
    redis_central_db: int = 3

    redis_local_host: str = "redis"
    redis_local_port: int = 6379
    redis_local_db: int = 4


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
