import os
import tempfile

import pytest

from app import create_app
from app.db import init_db, drop_db


@pytest.fixture(scope="function")
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()

    yield app
    with app.app_context():
        drop_db()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class Beers(object):
    def __init__(self, client):
        self._client = client

    def beers_list(self):
        return self._client.get(
            '/beers/',
        )

    def beer_detail(self, pk: int):
        return self._client.get('/beers/1/')
