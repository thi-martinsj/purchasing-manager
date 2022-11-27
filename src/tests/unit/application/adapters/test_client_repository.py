import pytest

from purchasing_manager import db
from purchasing_manager.application.adapters.client import ClientRepository
from purchasing_manager.application.exceptions import DatabaseException
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
