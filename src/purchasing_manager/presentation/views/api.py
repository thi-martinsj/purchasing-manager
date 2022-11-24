from flask import Blueprint
from flask_restx import Api

from .common import Index

common_bp = Blueprint("common", __name__, url_prefix="/api")

api = Api(
    common_bp,
    title="Purchasing Manager",
    description="Purchasing Manager API",
    doc="/docs/swagger",
)

common_ns = api.namespace("", description="Purchasing Manager API endpoints")
common_ns.add_resource(Index, "/", "/healthz")
