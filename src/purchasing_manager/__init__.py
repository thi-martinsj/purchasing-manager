import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import set_app_config
from .presentation.views.api import health_bp

load_dotenv()
DEPLOY_ENV = os.environ.get("DEPLOY_ENV", "Development")


app_path = os.path.dirname(os.path.abspath(__file__))
db = SQLAlchemy(session_options={"autoflush": False})
migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)

    set_app_config(app, DEPLOY_ENV)
    _register_blueprints(app)
    _set_database_config(app)

    return app


def _register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_bp)


def _set_database_config(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app=app, db=db, directory=os.path.join(app_path, "..", "migrations"))
