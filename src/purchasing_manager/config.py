import logging
import os

from dotenv import load_dotenv
from flask import Flask

from .application.exceptions import ConfigurationNotValid

load_dotenv()


class BaseConfig:
    LOGS_LEVEL = logging.INFO
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    VERSION = "1.0.0"


class DevelopmentConfig(BaseConfig):
    LOGS_LEVEL = logging.DEBUG


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    pass


def set_app_config(app: Flask) -> None:
    DEPLOY_ENV = os.environ.get("DEPLOY_ENV", "Development")

    try:
        config = {"Development": DevelopmentConfig, "Testing": TestingConfig, "Production": ProductionConfig}[
            DEPLOY_ENV
        ]

        app.config.from_object(config)
    except KeyError as e:
        raise ConfigurationNotValid() from e
