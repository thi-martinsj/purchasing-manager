from flask import Flask

from .application.exceptions import ConfigurationNotValid


class BaseConfig:
    VERSION = "1.0.0"


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


def set_app_config(app: Flask, mode: str) -> None:
    try:
        config = {"Development": DevelopmentConfig, "Testing": TestingConfig}[mode]

        app.config.from_object(config)
    except KeyError as e:
        raise ConfigurationNotValid() from e
