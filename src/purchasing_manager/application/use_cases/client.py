from purchasing_manager.application.adapters.client import ClientRepository
from purchasing_manager.domain.models.client import Client


class ClientUseCases:
    def get_clients(self, *args, **kwargs) -> list[Client]:
        clients_object = ClientRepository.list(**kwargs)

        if not clients_object:
            return {"message": "Clients not found"}, 404

        clients = [client.dict for client in clients_object]
        return clients
