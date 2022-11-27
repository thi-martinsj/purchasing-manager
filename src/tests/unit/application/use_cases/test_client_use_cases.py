from unittest.mock import patch

import pytest

from purchasing_manager.application.use_cases.client import ClientUseCases
from tests.doubles.stub import generate_clients_objects


@patch("purchasing_manager.application.adapters.client.ClientRepository.list")
def test_get_clients_return_a_list_of_clients(mock_list):
    clients = generate_clients_objects(3)
    mock_list.return_value = clients

    expected_response = [client.dict for client in clients]

    response = ClientUseCases().get_clients()

    assert expected_response == response


@pytest.mark.parametrize("list_response", [[], None])
@patch("purchasing_manager.application.adapters.client.ClientRepository.list")
def test_get_clients_return_clients_not_found(mock_list, list_response):
    mock_list.return_value = list_response

    expected_response = {"message": "Clients not found"}, 404

    response = ClientUseCases().get_clients()

    assert expected_response == response


@patch("purchasing_manager.application.adapters.client.ClientRepository.list")
def test_get_clients_raises_exception(mock_list):
    message = "Ohhh noooo :/"
    mock_list.side_effect = Exception(message)

    with pytest.raises(Exception) as e:
        ClientUseCases().get_clients()

    assert message == str(e.value)
