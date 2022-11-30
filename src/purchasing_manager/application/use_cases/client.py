from datetime import datetime
from http import HTTPStatus
from uuid import uuid4

from purchasing_manager.application.adapters.client import ClientRepository
from purchasing_manager.application.exceptions import (
    DuplicateError,
    MissingAttributeException,
    NotFoundException,
)
from purchasing_manager.domain.models.client import Client

NOT_FOUND_CLIENT_MESSAGE = dict(message="Clients not found")


class ClientUseCases:
    def get_clients(self, *args, **kwargs) -> list[dict[Client]]:
        clients_object = ClientRepository.list(**kwargs)

        if not clients_object:
            return NOT_FOUND_CLIENT_MESSAGE, HTTPStatus.NOT_FOUND

        clients = [client.dict for client in clients_object]
        return clients

    def retrieve(self, id: str) -> dict[Client]:
        client = ClientRepository.retrieve(id)

        if not client:
            return NOT_FOUND_CLIENT_MESSAGE, HTTPStatus.NOT_FOUND

        return client.dict

    def create(self, **kwargs) -> tuple[dict[Client], HTTPStatus]:
        try:
            client = ClientUseCases._create_client_object(**kwargs)
            ClientRepository.create(client)

            return client.dict, HTTPStatus.CREATED
        except MissingAttributeException as e:
            return dict(message=str(e)), HTTPStatus.BAD_REQUEST
        except DuplicateError as e:
            return dict(message=str(e)), HTTPStatus.BAD_REQUEST
        except Exception as e:
            raise e

    def update(self, **kwargs) -> dict[Client]:
        ClientUseCases._get_attribute_or_raise_exception("id", **kwargs)
        fields = ClientUseCases._delete_unwanted_fields(*["created_dt", "updated_dt", "document"], **kwargs)

        if "full_name" in fields:
            fields["name"] = fields.get("full_name")
            fields.pop("full_name")

        try:
            client = Client(**fields)
        except TypeError as e:
            return dict(message=str(e)), HTTPStatus.BAD_REQUEST

        try:
            new_client = ClientRepository.update(client)
        except NotFoundException:
            return NOT_FOUND_CLIENT_MESSAGE, HTTPStatus.NOT_FOUND

        return new_client.dict

    def delete(self, id: str) -> tuple[None, HTTPStatus]:
        try:
            ClientRepository.delete(id)
        except NotFoundException:
            return NOT_FOUND_CLIENT_MESSAGE, HTTPStatus.NOT_FOUND

        return None, HTTPStatus.NO_CONTENT

    @classmethod
    def _create_client_object(cls, **kwargs) -> Client:
        attrs = dict(
            id=str(uuid4()),
            created_dt=datetime.utcnow(),
            updated_dt=datetime.utcnow(),
            name=cls._get_attribute_or_raise_exception("full_name", **kwargs).title(),
            document=cls._get_attribute_or_raise_exception("document", **kwargs),
            phone=cls._get_attribute_or_raise_exception("phone", **kwargs),
            email=cls._get_attribute_or_raise_exception("email", **kwargs),
        )

        return Client(**attrs)

    @classmethod
    def _get_attribute_or_raise_exception(cls, attr, **kwargs) -> str:
        if attr in kwargs:
            return kwargs.get(attr)

        raise MissingAttributeException(f"Missing the following attribute: '{attr}'")

    @classmethod
    def _delete_unwanted_fields(cls, *args, **kwargs) -> dict:
        new_kwargs = kwargs

        for arg in args:
            if arg in new_kwargs:
                new_kwargs.pop(arg)

        return new_kwargs
