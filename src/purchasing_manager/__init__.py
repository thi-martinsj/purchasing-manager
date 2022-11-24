import os

from dotenv import load_dotenv
from flask import Flask

from .config import set_app_config
from .presentation.views.api import common_bp

load_dotenv()
DEPLOY_ENV = os.environ.get("DEPLOY_ENV", "Development")


def create_app() -> Flask:
    app = Flask(__name__)

    set_app_config(app, DEPLOY_ENV)
    _register_blueprints(app)

    return app


def _register_blueprints(app: Flask) -> None:
    app.register_blueprint(common_bp)
