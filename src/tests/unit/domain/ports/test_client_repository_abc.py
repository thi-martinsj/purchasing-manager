from uuid import uuid4

import pytest

from purchasing_manager.domain.ports.client import ClientRepositoryABC


def test_list_must_raises_exception():
    with pytest.raises(NotImplementedError):
        ClientRepositoryABC.list()


def test_retrieve_must_raises_exception():
    with pytest.raises(NotImplementedError):
        ClientRepositoryABC.retrieve(str(uuid4()))
