import os

import pytest

from purchasing_manager import create_app, db


@pytest.fixture
def app():
    os.environ["DEPLOY_ENV"] = "Testing"

    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()
        db.session.rollback()


@pytest.fixture
def api_client(app):
    with app.test_client() as client:
        return client
