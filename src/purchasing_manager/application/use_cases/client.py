from http import HTTPStatus

from purchasing_manager.application.adapters.client import ClientRepository
from purchasing_manager.domain.models.client import Client

NOT_FOUND_CLIENT_MESSAGE = {"message": "Clients not found"}


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
