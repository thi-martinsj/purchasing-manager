import json
import logging

from sqlalchemy.exc import IntegrityError

from purchasing_manager import db
from purchasing_manager.application.exceptions import (
    DatabaseException,
    DuplicateError,
    NotFoundException,
)
from purchasing_manager.domain.models.client import Client
from purchasing_manager.domain.ports.client import ClientRepositoryABC

logger = logging.getLogger(f"purchasing-manager.{__name__}")


class ClientRepository(ClientRepositoryABC):
    @classmethod
    def list(cls, offset: int = 0, limit: int = 100, **kwargs) -> list[Client]:
        try:
            logger.info(
                "Trying to retrieve a list of clients from database",
                extra={"props": {"table": "client", "filters": json.dumps(kwargs), "offset": offset, "limit": limit}},
            )
            return Client.query.filter_by(**kwargs).offset(offset).limit(limit).all()
        except Exception as e:
            message = "Error when trying to retrieve a list of clients from database"
            logger.exception(
                message,
                extra={
                    "props": {"table": "client", "filters": json.dumps(kwargs), "exception": str(e)},
                },
            )
            raise DatabaseException(message)

    @classmethod
    def retrieve(cls, id: str) -> Client:
        try:
            logger.info("Trying to retrieve a client from database", extra={"props": {"table": "client", "id": id}})
            client = Client.query.filter_by(id=id)

            if client.count() > 0:
                return client.one()

            return None

        except Exception as e:
            message = "Error when trying to retrieve a client from database"
            logger.exception(message, extra={"props": {"table": "client", "id": id, "exception": str(e)}})
            raise DatabaseException(message)

    @classmethod
    def create(cls, client: Client) -> None:
        try:
            logger.info(
                "Trying to save a new client in database",
                extra={"propos": {"table": "client", "client": client.dict}},
            )

            db.session.add(client)
            db.session.commit()
        except IntegrityError as e:
            message = "User already added in database"
            logger.exception(message, extra={"propos": {"table": "client", "client": client.dict, "exception": str(e)}})
            raise DuplicateError(message)
        except Exception as e:
            message = "Error when trying to save a new client in database"
            logger.exception(message, extra={"propos": {"table": "client", "client": client.dict, "exception": str(e)}})
            raise DatabaseException(message)

    @classmethod
    def update(cls, client: Client) -> Client:
        try:
            logger.info(
                f"Trying to update a client with id '{client.id}' in database",
                extra={"props": {"table": "client", "client": client.dict}},
            )

            old_client = Client.query.filter_by(id=client.id).first()

            if not old_client:
                raise NotFoundException("Client not found")

            if client.name:
                old_client.name = client.name.title()
            if client.phone:
                old_client.phone = client.phone
            if client.email:
                old_client.email = client.email

            db.session.commit()

            return Client.query.filter_by(id=client.id).first()
        except NotFoundException as e:
            message = f"Error when trying to update a client with id '{client.id}' in database. Client not found."
            logger.exception(message, extra={"propos": {"table": "client", "client": client.dict, "exception": str(e)}})
            raise e
        except Exception as e:
            message = f"Error when trying to update a client with id '{client.id}' in database"
            logger.exception(message, extra={"propos": {"table": "client", "client": client.dict, "exception": str(e)}})
            raise DatabaseException(message)

    @classmethod
    def delete(cls, id: str) -> None:
        try:
            logger.info(
                f"Trying to delete a client with id '{id}' in database",
                extra={"props": {"table": "client", "id": id}},
            )

            client = Client.query.filter_by(id=id).first()

            if not client:
                raise NotFoundException("Client not found")

            db.session.delete(client)
            db.session.commit()
        except NotFoundException as e:
            message = f"Error when trying to delete a client with id '{id}' in database. Client not found."
            logger.exception(message, extra={"propos": {"table": "client", "id": id, "exception": str(e)}})
            raise e
        except Exception as e:
            message = f"Error when trying to delete a client with id '{id}' in database"
            logger.exception(message, extra={"propos": {"table": "client", "id": id, "exception": str(e)}})
            raise DatabaseException(message)
