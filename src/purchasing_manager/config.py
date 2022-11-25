import os

from flask import Flask

from .application.exceptions import ConfigurationNotValid


class BaseConfig:
    VERSION = "1.0.0"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "postgresql://"


def set_app_config(app: Flask, mode: str) -> None:
    try:
        config = {"Development": DevelopmentConfig, "Testing": TestingConfig}[mode]

        app.config.from_object(config)
    except KeyError as e:
        raise ConfigurationNotValid() from e
