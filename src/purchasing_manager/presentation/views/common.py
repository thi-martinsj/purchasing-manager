from flask import current_app as app
from flask_restx import Resource


class Index(Resource):
    def get(self) -> dict:
        return dict(service="Purchasing Manager", version=app.config["VERSION"])
