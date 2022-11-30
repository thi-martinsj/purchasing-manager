from http import HTTPStatus
from unittest.mock import patch

from purchasing_manager import db
from purchasing_manager.application.adapters.client import ClientRepository
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


def test_create_a_new_client_must_return_201(api_client):
    client = generate_clients_objects(1)[0]
    payload = client.dict
    payload["full_name"] = client.name

    response = api_client.post("/api/client", headers={"Content-Type": "application/json"}, json=payload)
    response_json = response.json

    assert HTTPStatus.CREATED == response.status_code
    assert client.name.title() == response_json["name"]
    assert client.document == response_json["document"]
    assert 1 == len(ClientRepository.list())


def test_create_a_new_client_must_return_400_when_some_attribute_is_missing(api_client):
    payload = {}
    expected_message = dict(message="Missing the following attribute: 'full_name'")

    response = api_client.post("/api/client", headers={"Content-Type": "application/json"}, json=payload)

    assert HTTPStatus.BAD_REQUEST == response.status_code
    assert expected_message == response.json
    assert 0 == len(ClientRepository.list())


def test_create_a_new_client_must_return_400_when_client_already_created(api_client):
    expected_response = dict(message="User already added in database")
    client = generate_clients_objects(1)[0]
    payload = client.dict
    payload["full_name"] = client.name

    response_1 = api_client.post("/api/client", headers={"Content-Type": "application/json"}, json=payload)

    response_2 = api_client.post("/api/client", headers={"Content-Type": "application/json"}, json=payload)

    db.session.rollback()

    assert HTTPStatus.CREATED == response_1.status_code
    assert client.document == response_1.json["document"]
    assert HTTPStatus.BAD_REQUEST == response_2.status_code
    assert expected_response == response_2.json
    assert 1 == len(ClientRepository.list())


@patch("purchasing_manager.application.adapters.client.ClientRepository.create")
def test_create_a_new_client_must_return_500_when_some_unknown_exception_is_raised(mock_create, api_client):
    mock_create.side_effect = Exception("I'm not an exception, I'm a feature :))))")

    client = generate_clients_objects(1)[0]
    payload = client.dict
    payload["full_name"] = client.name

    response = api_client.post("/api/client", headers={"Content-Type": "application/json"}, json=payload)

    assert HTTPStatus.INTERNAL_SERVER_ERROR == response.status_code
    assert INTERNAL_SERVER_ERROR_MESSAGE == response.json


def test_update_a_client_must_update_successfully_with_status_200(api_client):
    client = generate_clients_objects(1)[0]
    db.session.add(client)
    db.session.commit()

    id = client.id
    payload = dict(phone="11999887766", email="test@example.com", document="12345678910")

    response = api_client.patch(f"/api/client/{id}", headers={"Content-Type": "application/json"}, json=payload)
    response_json = response.json

    assert HTTPStatus.OK == response.status_code
    assert payload["phone"] == response_json["phone"]
    assert payload["email"] == response_json["email"]
    assert client.id == response_json["id"]
    assert client.document == response_json["document"]
    assert str(client.created_dt) == response_json["created_dt"]


def test_update_a_client_must_return_400_when_some_field_is_invalid(api_client):
    expect_response = dict(message="'xpto' is an invalid keyword argument for Client")
    client = generate_clients_objects(1)[0]
    db.session.add(client)
    db.session.commit()

    id = client.id
    payload = dict(phone="11999887766", xpto="test@example.com")

    response = api_client.patch(f"/api/client/{id}", headers={"Content-Type": "application/json"}, json=payload)

    assert HTTPStatus.BAD_REQUEST == response.status_code
    assert expect_response == response.json


def test_update_a_client_must_return_404_when_client_is_not_found(api_client):
    client = generate_clients_objects(1)[0]
    id = client.id
    payload = dict(phone="11999887766")

    response = api_client.patch(f"/api/client/{id}", headers={"Content-Type": "application/json"}, json=payload)

    assert HTTPStatus.NOT_FOUND == response.status_code
    assert NOT_FOUND_MESSAGE == response.json


@patch("purchasing_manager.application.adapters.client.ClientRepository.update")
def test_update_a_client_must_return_500_when_some_unknown_exception_is_thrown(mock_update, api_client):
    client = generate_clients_objects(1)[0]
    mock_update.side_effect = Exception("Guess who is here? :))))")
    id = client.id
    payload = dict(phone="11999887766")

    response = api_client.patch(f"/api/client/{id}", headers={"Content-Type": "application/json"}, json=payload)

    assert HTTPStatus.INTERNAL_SERVER_ERROR == response.status_code
    assert INTERNAL_SERVER_ERROR_MESSAGE == response.json


def test_delete_client_must_return_successfully_with_status_204(api_client):
    client = generate_clients_objects(1)[0]

    db.session.add(client)
    db.session.commit()

    assert 1 == len(ClientRepository.list())

    response = api_client.delete(f"/api/client/{client.id}")

    assert 0 == len(ClientRepository.list())
    assert HTTPStatus.NO_CONTENT == response.status_code


def test_delete_client_must_return_404_when_client_is_not_found(api_client):
    clients = generate_clients_objects(2)

    db.session.add(clients[0])
    db.session.commit()

    assert 1 == len(ClientRepository.list())

    response = api_client.delete(f"/api/client/{clients[1].id}")

    assert 1 == len(ClientRepository.list())
    assert HTTPStatus.NOT_FOUND == response.status_code
    assert NOT_FOUND_MESSAGE == response.json


@patch("purchasing_manager.application.adapters.client.ClientRepository.delete")
def test_delete_client_must_return_500_when_some_unknown_exception_is_raised(mock_delete, api_client):
    mock_delete.side_effect = Exception("You won't delete my brother lol")
    client = generate_clients_objects(1)[0]

    db.session.add(client)
    db.session.commit()

    assert 1 == len(ClientRepository.list())

    response = api_client.delete(f"/api/client/{client.id}")

    assert 1 == len(ClientRepository.list())
    assert HTTPStatus.INTERNAL_SERVER_ERROR == response.status_code
    assert INTERNAL_SERVER_ERROR_MESSAGE == response.json
