from unittest.mock import Mock

import pytest

from purchasing_manager.domain.ports.client import ClientRepositoryABC


def test_list_must_raises_exception():
    with pytest.raises(NotImplementedError):
        ClientRepositoryABC.list()


def test_retrieve_must_raises_exception():
    with pytest.raises(NotImplementedError):
        ClientRepositoryABC.retrieve(Mock())


def test_create_must_raises_exception():
    with pytest.raises(NotImplementedError):
        ClientRepositoryABC.create(Mock())
