import pytest

from purchasing_manager.domain.ports.client import ClientRepositoryABC


def test_list_must_raises_exception():
    with pytest.raises(NotImplementedError):
        ClientRepositoryABC.list()
