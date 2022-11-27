import logging
import os
import sys

import json_logging
from dotenv import load_dotenv
from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import set_app_config

load_dotenv()
DEPLOY_ENV = os.environ.get("DEPLOY_ENV", "Development")


app_path = os.path.dirname(os.path.abspath(__file__))
db = SQLAlchemy(session_options={"autoflush": False})
logger = logging.getLogger("purchasing-manager")
migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)

    set_app_config(app, DEPLOY_ENV)
    _set_database_config(app)
    _configure_logger(app)
    _register_blueprints(app)

    return app


def _register_blueprints(app: Flask) -> None:
    from .presentation.views.api import health_bp
    from .presentation.views.client import client_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(client_bp)


def _set_database_config(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app=app, db=db, directory=os.path.join(app_path, "..", "migrations"))


def _configure_logger(app: Flask) -> None:
    if not json_logging.ENABLE_JSON_LOGGING:
        json_logging.init_flask(enable_json=True)
        json_logging.init_request_instrument(app)

        logger.setLevel(app.config["LOGS_LEVEL"])
        logger.addHandler(logging.StreamHandler(sys.stdout))

    @app.before_request
    def log_request():
        logger.info(
            "Request received",
            extra={"props": {"path": request.path, "method": request.method}},
        )

    @app.after_request
    def log_response(response):
        logger = logging.getLogger("purhasing-manager")
        logger.info(
            "Request response",
            extra={
                "props": {
                    "path": request.path,
                    "method": request.method,
                    "status": response.status_code,
                }
            },
        )

        return response
