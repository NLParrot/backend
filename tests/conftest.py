import pytest
from chatapp.responses.select_response import SelectResponse
from chatapp.wsgi import app as flask_app

@pytest.fixture()
def app():
    flask_app.config.update({
        "TESTING": True,
    })

    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def select_response():
    return SelectResponse()
