from unittest.mock import MagicMock
import pytest
from app import app as flask_app


@pytest.fixture
def app():
    """
    Configures the Flask application for testing
    """
    flask_app.config.update({"TESTING": True, "SECRET_KEY": "test_secret_key"})
    yield flask_app


@pytest.fixture
# pylint: disable-next=redefined-outer-name
def client(app):
    """
    Creates a test client
    """
    return app.test_client()


@pytest.fixture
def mock_db_connection(mocker):
    """
    Mocks the database connection for testing
    """
    mock_conn = MagicMock()
    # Mock all the relevant places where the DB is sourced
    mocker.patch("config.database.get_db_connection", return_value=mock_conn)
    mocker.patch(
        "services.lancamentos_service.get_db_connection", return_value=mock_conn
    )
    mocker.patch("services.usuario_service.get_db_connection", return_value=mock_conn)

    return mock_conn
