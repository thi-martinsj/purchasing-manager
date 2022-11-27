from flask import Blueprint, request
from flask_restx import Api, Resource

from purchasing_manager.application.use_cases.client import ClientUseCases

from .schemas import client, internal_server_error, not_found_error

client_bp = Blueprint("Client", __name__, url_prefix="/api/client")

api = Api(client_bp, title="Client", description="Client API", doc="/docs/swagger")

ns = api.namespace("", description="Client API endpoints")
ns.add_model(client.name, client)
ns.add_model(internal_server_error.name, internal_server_error)
ns.add_model(not_found_error.name, not_found_error)


@ns.route("")
class Client(Resource):
    @ns.response(200, "List all clients", [client])
    @ns.response(404, "Clients not found", not_found_error)
    @ns.response(500, "Internal server error", internal_server_error)
    @ns.param("document")
    @ns.param("email")
    def get(self) -> list[client]:
        params = request.args

        client = ClientUseCases()
        return client.get_clients(**params)
