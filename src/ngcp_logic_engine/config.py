"""ngcp-logic-engine  settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """common configs."""

    env: str = "development"

    model_config = SettingsConfigDict(env_prefix="logic_engine_")


class DevelopmentConfig(BaseConfig):
    """configs for development."""


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
