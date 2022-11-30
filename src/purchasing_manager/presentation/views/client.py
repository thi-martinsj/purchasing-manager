from flask import Blueprint, request
from flask_restx import Api, Resource

from purchasing_manager.application.use_cases.client import ClientUseCases

from .schemas import client, internal_server_error, invalid_payload, not_found_error

client_bp = Blueprint("Client", __name__, url_prefix="/api/client")

api = Api(client_bp, title="Client", description="Client API", doc="/docs/swagger")

ns = api.namespace("", description="Client API endpoints")
ns.add_model(client.name, client)
ns.add_model(internal_server_error.name, internal_server_error)
ns.add_model(not_found_error.name, not_found_error)
ns.add_model(invalid_payload.name, invalid_payload)


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

    @ns.response(201, "Client object", client)
    @ns.response(400, "Invalid payload", invalid_payload)
    @ns.response(500, "Internal server error", internal_server_error)
    @ns.expect(client)
    def post(self):
        kwargs = request.get_json()
        client = ClientUseCases()
        return client.create(**kwargs)


@ns.route("/<uuid:id>")
class SpecificClient(Resource):
    @ns.response(200, "Client object", client)
    @ns.response(404, "Client not found", not_found_error)
    @ns.response(500, "Internal server error", internal_server_error)
    def get(self, id) -> client:
        client = ClientUseCases()
        return client.retrieve(str(id))

    @ns.response(200, "Client object", client)
    @ns.response(400, "Invalid payload", invalid_payload)
    @ns.response(404, "Client not found", not_found_error)
    @ns.response(500, "Internal server error", internal_server_error)
    @ns.expect(client)
    def patch(self, id) -> client:
        kwargs = request.get_json()
        kwargs["id"] = str(id)
        client = ClientUseCases()
        return client.update(**kwargs)

    @ns.response(204, "Client deleted with sucess")
    @ns.response(404, "Client not found", not_found_error)
    @ns.response(500, "Internal server error", internal_server_error)
    def delete(self, id) -> None:
        client = ClientUseCases()
        return client.delete(str(id))
