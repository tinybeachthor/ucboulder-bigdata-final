import pytest
from .web import create_app

@pytest.fixture()
def app():
    app = create_app()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


def test_healthz(client):
    response = client.get('/healthz')
    assert b'ok' == response.data

def test_metrics(client):
    response = client.get('/metrics')
    assert b'GET index' in response.data
    assert b'GET index duration' in response.data
