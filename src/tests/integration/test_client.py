from http import HTTPStatus
from unittest.mock import patch

from purchasing_manager import db
from tests.doubles.stub import generate_clients_objects

NOT_FOUND_MESSAGE = dict(message="Clients not found")
INTERNAL_SERVER_ERROR_MESSAGE = dict(message="Internal Server Error")


def test_get_clients_return_a_list_of_clients(api_client):
    clients = generate_clients_objects(5)

    for client in clients:
        db.session.add(client)
        db.session.commit()

    response = api_client.get("/api/client")

    assert HTTPStatus.OK == response.status_code
    assert 5 == len(response.json)


def test_get_clients_return_client_from_document(api_client):
    clients = generate_clients_objects(5)
    document = clients[0].document

    for client in clients:
        db.session.add(client)
        db.session.commit()

    response = api_client.get(f"/api/client?document={document}")

    assert HTTPStatus.OK == response.status_code
    assert 1 == len(response.json)


def test_get_clients_must_return_404(api_client):
    response = api_client.get("/api/client")

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert NOT_FOUND_MESSAGE == response.json


@patch("purchasing_manager.application.adapters.client.ClientRepository.list")
def test_get_clients_must_return_500(mock_list, api_client):
    mock_list.side_effect = Exception("Ohh nooo :(")

    response = api_client.get("/api/client")

    assert HTTPStatus.INTERNAL_SERVER_ERROR == response.status_code
    assert INTERNAL_SERVER_ERROR_MESSAGE == response.json


def test_get_client_must_return_a_client(api_client):
    clients = generate_clients_objects(2)
    except_response = clients[0].dict

    for client in clients:
        db.session.add(client)
        db.session.commit()

    response = api_client.get(f"/api/client/{clients[0].id}")

    assert HTTPStatus.OK == response.status_code
    assert except_response == response.json


def test_get_client_must_return_404(api_client):
    response = api_client.get("/api/client/4fd36341-ab6e-4c2d-a0d4-de39207f88a4")

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert NOT_FOUND_MESSAGE == response.json


@patch("purchasing_manager.application.adapters.client.ClientRepository.retrieve")
def test_get_client_must_return_500(mock_retrieve, api_client):
    mock_retrieve.side_effect = Exception("Ohh my God :(")

    response = api_client.get("/api/client/4fd36341-ab6e-4c2d-a0d4-de39207f88a4")

    assert HTTPStatus.INTERNAL_SERVER_ERROR == response.status_code
    assert INTERNAL_SERVER_ERROR_MESSAGE == response.json
