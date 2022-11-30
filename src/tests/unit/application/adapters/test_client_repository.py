from unittest.mock import Mock, patch

import pytest
from sqlalchemy.exc import IntegrityError

from purchasing_manager import db
from purchasing_manager.application.adapters.client import ClientRepository
from purchasing_manager.application.exceptions import (
    DatabaseException,
    DuplicateError,
    NotFoundException,
)
from purchasing_manager.domain.models.client import Client
from tests.doubles.stub import generate_clients_objects


def test_list_all_clients_without_filters_and_limit_and_offset(app):
    clients_obj = generate_clients_objects(2)
    expected_response = []

    for client in clients_obj:
        expected_response.append(client.dict)
        db.session.add(client)
        db.session.commit()

    clients = ClientRepository.list()

    result = [client.dict for client in clients]

    assert expected_response == result
    assert 2 == len(clients)


def test_list_clients_with_limit(app):
    clients_obj = generate_clients_objects(3)
    expected_response = [clients_obj[0].dict]

    for client in clients_obj:
        db.session.add(client)
        db.session.commit()

    clients = ClientRepository.list(limit=1)

    result = [client.dict for client in clients]

    assert expected_response == result
    assert 1 == len(clients)


def test_list_clients_with_offset(app):
    clients_obj = generate_clients_objects(3)
    expected_response = [clients_obj[1].dict, clients_obj[2].dict]

    for client in clients_obj:
        db.session.add(client)
        db.session.commit()

    clients = ClientRepository.list(offset=1)

    result = [client.dict for client in clients]

    assert expected_response == result
    assert 2 == len(clients)


def test_list_clients_with_offset_and_limit(app):
    clients_obj = generate_clients_objects(4)
    expected_response = [clients_obj[1].dict, clients_obj[2].dict]

    for client in clients_obj:
        db.session.add(client)
        db.session.commit()

    clients = ClientRepository.list(offset=1, limit=2)

    result = [client.dict for client in clients]

    assert expected_response == result
    assert 2 == len(clients)


@pytest.mark.parametrize(["filter", "ind_client"], [["document", 0], ["email", 1], ["phone", 2]])
def test_list_clients_with_filters(app, filter, ind_client):
    clients_obj = generate_clients_objects(4)
    expected_response = [clients_obj[ind_client].dict]

    for client in clients_obj:
        db.session.add(client)
        db.session.commit()

    kwargs = {filter: expected_response[0][filter]}

    clients = ClientRepository.list(**kwargs)

    result = [client.dict for client in clients]

    assert expected_response == result
    assert 1 == len(clients)


def test_list_clients_no_clients(app):
    clients = ClientRepository.list()

    assert 0 == len(clients)


def test_list_clients_raise_exception(app):
    message = "Error when trying to retrieve a list of clients from database"

    with pytest.raises(DatabaseException) as e:
        ClientRepository.list(limit="xpto")

    assert message == str(e.value)


def test_retrieve_client_must_return_with_success(app):
    clients_obj = generate_clients_objects(2)
    expected_response = clients_obj[1].dict

    for client in clients_obj:
        db.session.add(client)
        db.session.commit()

    client = ClientRepository.retrieve(clients_obj[1].id)

    assert expected_response == client.dict


def test_retrieve_client_must_return_none(app):
    clients_obj = generate_clients_objects(1)

    db.session.add(clients_obj[0])
    db.session.commit()

    client = ClientRepository.retrieve("xpto")

    assert client is None


def test_retrieve_client_raise_exception():
    message = "Error when trying to retrieve a client from database"

    with pytest.raises(DatabaseException) as e:
        ClientRepository.retrieve("foo")

    assert message == str(e.value)


def test_create_client_must_add_with_success(app):
    client = generate_clients_objects(1)[0]

    ClientRepository().create(client)

    client_obj = ClientRepository.retrieve(client.id)
    all_clients = ClientRepository.list()

    assert client.dict == client_obj.dict
    assert 1 == len(all_clients)


def test_create_client_cant_add_2_clients_with_the_same_document(app):
    client = generate_clients_objects(1)[0]

    ClientRepository().create(client)
    ClientRepository().create(client)

    all_clients = ClientRepository().list()

    assert 1 == len(all_clients)


@patch("purchasing_manager.db.session.add")
def test_create_client_raise_integrity_error(mock_add, app):
    mock_add.side_effect = IntegrityError(Mock(), Mock(), Mock())
    message = "User already added in database"

    with pytest.raises(DuplicateError) as e:
        ClientRepository().create(Mock())

    assert message == str(e.value)
    assert 0 == len(ClientRepository().list())


def test_create_client_raise_exception(app):
    message = "Error when trying to save a new client in database"

    with pytest.raises(Exception) as e:
        ClientRepository().create(Mock())

    assert message == str(e.value)
    assert 0 == len(ClientRepository().list())


@pytest.mark.parametrize(
    "attrs_to_update",
    [[], ["name"], ["phone"], ["email"], ["name", "phone"], ["phone", "email"], ["name", "phone", "email"]],
)
def test_update_client_must_update_with_success(attrs_to_update, app):
    def _add_client():
        client = generate_clients_objects(1)[0]

        db.session.add(client)
        db.session.commit()

        return client.dict

    old_client = _add_client()

    new_client = Client(id=old_client["id"])

    if "name" in attrs_to_update:
        new_client.name = "Fulano Beltrano"

    if "phone" in attrs_to_update:
        new_client.phone = "11999887766"

    if "email" in attrs_to_update:
        new_client.email = "beltrano@test.com"

    response = ClientRepository().update(new_client)

    assert old_client["id"] == response.id
    assert old_client["document"] == response.document

    if "name" in attrs_to_update:
        assert new_client.name == response.name
        assert old_client["name"] != response.name

    if "phone" in attrs_to_update:
        assert new_client.phone == response.phone
        assert old_client["phone"] != response.phone

    if "email" in attrs_to_update:
        assert new_client.email == response.email
        assert old_client["email"] != response.email


def test_update_client_raise_not_found_exception_when_client_is_not_found(app):
    message = "Client not found"
    client = generate_clients_objects(1)[0]

    with pytest.raises(NotFoundException) as e:
        ClientRepository().update(client)

    assert message == str(e.value)


@patch("purchasing_manager.application.adapters.client.logger.info")
def test_update_client_raise_database_exception_when_some_unknown_exception_is_raised(mock_logger, app):
    def _add_client():
        client = generate_clients_objects(1)[0]

        db.session.add(client)
        db.session.commit()

        return client.dict

    mock_logger.side_effect = Exception("Hello, I'm hereeee ;D")
    old_client = _add_client()

    new_client = Client(**old_client)

    message = f"Error when trying to update a client with id '{old_client['id']}' in database"

    with pytest.raises(DatabaseException) as e:
        ClientRepository().update(new_client)

    assert message == str(e.value)


def test_delete_client_must_delete_successfully(app):
    client = generate_clients_objects(1)[0]

    db.session.add(client)
    db.session.commit()

    assert 1 == len(ClientRepository.list())

    ClientRepository.delete(client.id)

    assert 0 == len(ClientRepository.list())


def test_delete_client_must_raise_not_found_exception_when_client_is_not_in_database(app):
    clients = generate_clients_objects(3)
    message = "Client not found"

    for client in clients[1:]:
        db.session.add(client)
        db.session.commit()

    assert 2 == len(ClientRepository.list())

    with pytest.raises(NotFoundException) as e:
        ClientRepository.delete(clients[0].id)

    assert message == str(e.value)
    assert 2 == len(ClientRepository.list())


@patch("purchasing_manager.db.session.delete")
def test_delete_client_must_raise_database_exception_when_some_unknown_exception_is_raised(mock_delete, app):
    mock_delete.side_effect = Exception("It's not a bug. It's feature")
    client = generate_clients_objects(1)[0]
    message = f"Error when trying to delete a client with id '{client.id}' in database"

    db.session.add(client)
    db.session.commit()

    with pytest.raises(DatabaseException) as e:
        ClientRepository.delete(client.id)

    assert message == str(e.value)
