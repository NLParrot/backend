import pytest
from chatapp.wsgi import app

@pytest.fixture()
def app():
    flask_app.config.update({
        "TESTING": True,
    })

    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


