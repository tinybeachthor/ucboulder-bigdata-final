import pytest
from .web import app as flask_app

@pytest.fixture()
def app():
    app = flask_app
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_healthz(client):
    response = client.get('/healthz')
    assert b'ok' == response.data
