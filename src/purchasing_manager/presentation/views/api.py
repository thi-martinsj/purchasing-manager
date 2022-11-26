from flask import Blueprint
from flask import current_app as app
from flask_restx import Api, Resource

from .schemas import health

health_bp = Blueprint("Health", __name__, url_prefix="/api")

api = Api(
    health_bp,
    title="Purchasing Manager",
    description="Purchasing Manager API",
    doc="/docs/swagger",
)

ns = api.namespace("", description="Purchasing Manager API endpoints")
ns.add_model(health.name, health)


@ns.response(200, "OK", health)
@ns.route("", "/healthz")
class Index(Resource):
    def get(self) -> dict:
        return dict(service="Purchasing Manager", version=app.config["VERSION"])
