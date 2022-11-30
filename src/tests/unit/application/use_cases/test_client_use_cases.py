from http import HTTPStatus
from unittest.mock import patch

import pytest

from purchasing_manager.application.exceptions import (
    DuplicateError,
    MissingAttributeException,
    NotFoundException,
)
from purchasing_manager.application.use_cases.client import ClientUseCases
from tests.doubles.stub import generate_clients_objects

NOT_FOUND_MESSAGE = dict(message="Clients not found")


@patch("purchasing_manager.application.adapters.client.ClientRepository.list")
def test_get_clients_return_a_list_of_clients(mock_list):
    clients = generate_clients_objects(3)
    mock_list.return_value = clients

    expected_response = [client.dict for client in clients]

    response = ClientUseCases().get_clients()

    assert expected_response == response


@pytest.mark.parametrize("list_response", [[], None])
@patch("purchasing_manager.application.adapters.client.ClientRepository.list")
def test_get_clients_return_not_found(mock_list, list_response):
    mock_list.return_value = list_response

    expected_response = NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND

    response = ClientUseCases().get_clients()

    assert expected_response == response


@patch("purchasing_manager.application.adapters.client.ClientRepository.list")
def test_get_clients_raises_exception(mock_list):
    message = "Ohhh noooo :/"
    mock_list.side_effect = Exception(message)

    with pytest.raises(Exception) as e:
        ClientUseCases().get_clients()

    assert message == str(e.value)


@patch("purchasing_manager.application.adapters.client.ClientRepository.retrieve")
def test_retrieve_return_a_client(mock_retrieve):
    client = generate_clients_objects(1)[0]
    mock_retrieve.return_value = client

    response = ClientUseCases().retrieve("foo")

    assert client.dict == response


@patch("purchasing_manager.application.adapters.client.ClientRepository.retrieve")
def test_retrieve_return_not_found(mock_retrieve):
    mock_retrieve.return_value = None
    expected_response = NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND

    response = ClientUseCases().retrieve("xpto")

    assert expected_response == response


@patch("purchasing_manager.application.adapters.client.ClientRepository.retrieve")
def test_retrieve_raises_exception(mock_retrieve):
    message = "Aff...."
    mock_retrieve.side_effect = Exception(message)

    with pytest.raises(Exception) as e:
        ClientUseCases().retrieve("xpto")

    assert message == str(e.value)


@patch("purchasing_manager.application.use_cases.client.ClientUseCases._create_client_object")
@patch("purchasing_manager.application.adapters.client.ClientRepository.create")
def test_create_must_create_with_success_and_return_201(mock_create, mock_create_client_object):
    client = generate_clients_objects(1)[0]
    expected_response = client.dict, HTTPStatus.CREATED

    mock_create_client_object.return_value = client

    response = ClientUseCases().create(**client.dict)

    mock_create_client_object.assert_called_once_with(**client.dict)
    mock_create.assert_called_once_with(client)
    assert expected_response == response


@patch("purchasing_manager.application.use_cases.client.ClientUseCases._create_client_object")
@patch("purchasing_manager.application.adapters.client.ClientRepository.create")
def test_create_must_return_400_when_missing_attribute_exception_is_raised(mock_create, mock_create_client_object):
    mock_create_client_object.side_effect = MissingAttributeException("Oh noooo")
    expected_response = dict(message="Oh noooo"), HTTPStatus.BAD_REQUEST

    response = ClientUseCases().create(**{})

    mock_create.assert_not_called()
    assert expected_response == response


@patch("purchasing_manager.application.use_cases.client.ClientUseCases._create_client_object")
@patch("purchasing_manager.application.adapters.client.ClientRepository.create")
def test_create_must_return_400_when_duplicate_error_is_raised(mock_create, mock_create_client_object):
    client = generate_clients_objects(1)[0]

    mock_create.side_effect = DuplicateError("Aff, exception again :/")
    mock_create_client_object.return_value = client
    expected_response = dict(message="Aff, exception again :/"), HTTPStatus.BAD_REQUEST

    response = ClientUseCases().create(**client.dict)

    mock_create_client_object.assert_called_once_with(**client.dict)
    mock_create.assert_called_once_with(client)
    assert expected_response == response


@patch("purchasing_manager.application.use_cases.client.ClientUseCases._create_client_object")
@patch("purchasing_manager.application.adapters.client.ClientRepository.create")
def test_create_must_raise_exception_when_some_unknown_exception_is_raised(mock_create, mock_create_client_object):
    message = "One more. I'm tired :/"
    mock_create_client_object.side_effect = Exception(message)

    with pytest.raises(Exception) as e:
        ClientUseCases().create(**{})

        mock_create.assert_not_called()

    assert message == str(e.value)


@patch("purchasing_manager.application.use_cases.client.ClientUseCases._get_attribute_or_raise_exception")
def test_create_client_must_return_a_valid_client_object(mock_get_attr):
    mock_get_attr.return_value = "test"
    kwargs = {}

    client = ClientUseCases._create_client_object(**kwargs)

    assert 4 == mock_get_attr.call_count
    assert "Test" == client.name
    assert "test" == client.document
    assert "test" == client.phone
    assert "test" == client.email


@patch("purchasing_manager.application.use_cases.client.ClientUseCases._get_attribute_or_raise_exception")
def test_create_client_must_raise_missing_attribute_exception(mock_get_attr):
    message = "Exception: I'm here again :D"
    mock_get_attr.side_effect = MissingAttributeException(message)

    with pytest.raises(MissingAttributeException) as e:
        ClientUseCases._create_client_object(**{})

    assert message == str(e.value)


def test_get_attribute_return_string_successfully():
    kwargs = dict(foo="xpto")

    response = ClientUseCases._get_attribute_or_raise_exception("foo", **kwargs)

    assert "xpto" == response


@pytest.mark.parametrize("kwargs", [{}, dict(foo="xpto")])
def test_get_attribute_raises_exception(kwargs):
    message = "Missing the following attribute: 'abc'"

    with pytest.raises(MissingAttributeException) as e:
        ClientUseCases._get_attribute_or_raise_exception("abc", **kwargs)

    assert message == str(e.value)


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(id="xpto", document="12345678941", full_name="Ciclano"),
        dict(id="abc", phone="11999887766", email="test@example.com"),
        dict(),
    ],
)
@patch("purchasing_manager.application.use_cases.client.ClientUseCases._get_attribute_or_raise_exception")
@patch("purchasing_manager.application.use_cases.client.ClientUseCases._delete_unwanted_fields")
@patch("purchasing_manager.application.adapters.client.ClientRepository.update")
def test_update_must_update_success_and_return_dict(mock_update, mock_delete_fields, mock_get_attr, kwargs):
    default_kwargs = dict(kwargs)
    client = generate_clients_objects(1)[0]
    mock_delete_fields.return_value = kwargs
    mock_update.return_value = client

    response = ClientUseCases().update(**kwargs)

    mock_get_attr.assert_called_once_with("id", **default_kwargs)
    mock_delete_fields.assert_called_once_with(*["created_dt", "updated_dt", "document"], **default_kwargs)
    mock_update.assert_called_once()
    assert client.dict == response


@patch("purchasing_manager.application.use_cases.client.ClientUseCases._get_attribute_or_raise_exception")
@patch("purchasing_manager.application.use_cases.client.ClientUseCases._delete_unwanted_fields")
@patch("purchasing_manager.application.adapters.client.ClientRepository.update")
def test_update_must_return_bad_request_when_some_field_is_invalid(mock_update, mock_delete_fields, mock_get_attr):
    kwargs = dict(xpto="foo")
    mock_delete_fields.return_value = kwargs

    response = ClientUseCases().update(**kwargs)

    mock_get_attr.assert_called_once_with("id", **kwargs)
    mock_delete_fields.assert_called_once_with(*["created_dt", "updated_dt", "document"], **kwargs)
    mock_update.assert_not_called()
    assert HTTPStatus.BAD_REQUEST in response


@patch("purchasing_manager.application.use_cases.client.ClientUseCases._get_attribute_or_raise_exception")
@patch("purchasing_manager.application.use_cases.client.ClientUseCases._delete_unwanted_fields")
@patch("purchasing_manager.application.adapters.client.ClientRepository.update")
def test_update_must_return_not_found_when_some_client_is_not_found(mock_update, mock_delete_fields, mock_get_attr):
    kwargs = dict(phone="11999887766")
    mock_delete_fields.return_value = kwargs
    mock_update.side_effect = NotFoundException()

    response = ClientUseCases().update(**kwargs)

    mock_get_attr.assert_called_once_with("id", **kwargs)
    mock_delete_fields.assert_called_once_with(*["created_dt", "updated_dt", "document"], **kwargs)
    assert (dict(message="Clients not found"), HTTPStatus.NOT_FOUND) == response


@patch("purchasing_manager.application.use_cases.client.ClientUseCases._get_attribute_or_raise_exception")
@patch("purchasing_manager.application.use_cases.client.ClientUseCases._delete_unwanted_fields")
@patch("purchasing_manager.application.adapters.client.ClientRepository.update")
def test_update_must_raise_exception_when_some_unknown_exception_is_thrown(
    mock_update, mock_delete_fields, mock_get_attr
):
    message = "Did you think I wouldn't come back?"
    kwargs = dict(phone="11999887766")
    mock_delete_fields.return_value = kwargs
    mock_update.side_effect = Exception(message)

    with pytest.raises(Exception) as e:
        ClientUseCases().update(**kwargs)

    mock_get_attr.assert_called_once_with("id", **kwargs)
    mock_delete_fields.assert_called_once_with(*["created_dt", "updated_dt", "document"], **kwargs)
    assert message == str(e.value)


@pytest.mark.parametrize(
    ["args", "kwargs", "expected_response"],
    [
        [["xpto"], {"abc": 1, "xpto": 2}, {"abc": 1}],
        [["foo"], {"abc": 1, "xpto": 2}, {"abc": 1, "xpto": 2}],
        [["xpto", "foo"], {}, {}],
        [[], {"abc": 1, "xpto": 2}, {"abc": 1, "xpto": 2}],
        [[], {}, {}],
    ],
)
def test_delete_unwanted_fields_must_return_successfully(args, kwargs, expected_response):
    response = ClientUseCases()._delete_unwanted_fields(*args, **kwargs)

    assert expected_response == response
