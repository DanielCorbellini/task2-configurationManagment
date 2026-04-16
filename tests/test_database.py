import pytest
from config.database import get_db_connection

def test_real_db_connection_success():
    """
    Tests if the application can successfully establish a live connection to the PostgreSQL database.
    This test runs completely independently of the `mock_db_connection` fixture.
    """
    conn = None
    try:
        conn = get_db_connection()
        # Executes an extremely simple ping operation against the database
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result[0] == 1
    except Exception as e:
        pytest.fail(f"Erro na conexão com o banco de dados: {e}")
    finally:
        if conn is not None:
            conn.close()
