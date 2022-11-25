import os

import pytest

from purchasing_manager import create_app


@pytest.fixture
def app():
    os.environ["DEPLOY_ENV"] = "Testing"

    app = create_app()

    yield app


@pytest.fixture
def api_client(app):
    with app.test_client() as client:
        return client
