from abc import ABC

from purchasing_manager.domain.models.client import Client


class ClientRepositoryABC(ABC):
    @classmethod
    def list(cls, *args, **kwargs) -> list[Client]:
        raise NotImplementedError

    @classmethod
    def retrieve(cls, id: str) -> Client:
        raise NotImplementedError

    @classmethod
    def create(cls, client: Client) -> None:
        raise NotImplementedError

    @classmethod
    def update(cls, client: Client) -> Client:
        raise NotImplementedError

    @classmethod
    def delete(cls, id: str) -> None:
        raise NotImplementedError
