import pytest
import sys
import os

from app import app as flask_app
from unittest.mock import MagicMock

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test_secret_key"
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_db_connection(mocker):
    mock_conn = MagicMock()
    # Mock all the relevant places where the DB is sourced
    mocker.patch("config.database.get_db_connection", return_value=mock_conn)
    mocker.patch("services.lancamentos_service.get_db_connection", return_value=mock_conn)
    mocker.patch("services.usuario_service.get_db_connection", return_value=mock_conn)
    return mock_conn
