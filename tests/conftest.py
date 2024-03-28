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

@pytest.fixture()
def mock_open_toml(mocker):
    mock_open = mocker.mock_open(read_data=b"utter=['What are you doing, {name}?']\n variables=['name']")
    mocker.patch("builtins.open", mock_open)
    return mock_open

@pytest.fixture()
def mock_open_toml_novar(mocker):
    mock_open = mocker.mock_open(read_data=b"utter=['No names required']\n variables=[]")
    mocker.patch("builtins.open", mock_open)
    return mock_open

