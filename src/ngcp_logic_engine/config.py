"""ngcp-logic-engine  settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """common configs."""

    env: str = "development"

    model_config = SettingsConfigDict(env_prefix="logic_engine_")


class DevelopmentConfig(BaseConfig):
    """development config."""

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 3

    class Config:
        """Configuration subclass."""

        env_file = ".env"
        env_file_encoding = "utf-8"


class ProductionConfig(BaseConfig):
    """production config."""


class TestingConfig(BaseConfig):
    """configs for testing."""


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
