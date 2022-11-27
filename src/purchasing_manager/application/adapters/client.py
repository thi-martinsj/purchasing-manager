import json
import logging

from purchasing_manager.application.exceptions import DatabaseException
from purchasing_manager.domain.models.client import Client
from purchasing_manager.domain.ports.client import ClientRepositoryABC

logger = logging.getLogger(f"purchasing-manager.{__name__}")


class ClientRepository(ClientRepositoryABC):
    @classmethod
    def list(cls, offset: int = 0, limit: int = 100, **kwargs) -> list[Client]:
        try:
            logger.info(
                "Tring to retrieve a list of clients from database",
                extra={"props": {"table": "client", "filters": json.dumps(kwargs), "offset": offset, "limit": limit}},
            )
            return Client.query.filter_by(**kwargs).offset(offset).limit(limit)
        except Exception as e:
            message = "Error when trying to retrieve a list of clients from database"
            logger.error(
                message,
                extra={
                    "props": {"table": "client", "filters": json.dumps(kwargs), "exception": str(e)},
                },
            )
            raise DatabaseException(message)
