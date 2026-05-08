from services.usuario_service import autenticar_usuario, listar_usuarios
from services.lancamentos_service import (
    listar_lancamentos,
    inserir_lancamento,
    buscar_lancamento_por_id,
    atualizar_lancamento,
    deletar_lancamento_db,
)


def test_autenticar_usuario_valid(mock_db_connection, mocker):
    """
    Test authentication of valid user.
    """
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "nome": "admin",
        "senha": "202cb962ac59075b964b07152d234b70",
    }

    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor
    result = autenticar_usuario("admin", "123")

    assert result["id"] == 1
    mock_cursor.execute.assert_called_once()
    assert "admin" in mock_cursor.execute.call_args[0][1]


def test_autenticar_usuario_invalid(mock_db_connection, mocker):
    """
    Test authentication of invalid user.
    """
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor

    result = autenticar_usuario("admin", "wrong")
    assert result is None


def test_listar_usuarios(mock_db_connection, mocker):
    """
    Test listing users.
    """
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchall.return_value = [{"id": 1, "nome": "A"}]
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor

    result = listar_usuarios()
    assert len(result) == 1


def test_listar_lancamentos_filters(mock_db_connection, mocker):
    """
    Test listing launches with filters.
    """
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor

    listar_lancamentos(
        id_usuario=1, data_filtro="2024-01-01", situacao_filtro="EFETIVADO"
    )

    query = mock_cursor.execute.call_args[0][0]
    args = mock_cursor.execute.call_args[0][1]

    assert "id_usuario = %s" in query
    assert "data_lancamento = %s" in query
    assert "situacao = %s" in query
    assert args == (1, "2024-01-01", "EFETIVADO")


def test_inserir_lancamento(mock_db_connection, mocker):
    """
    Test inserting a launch.
    """
    mock_cursor = mocker.MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor

    result = inserir_lancamento(
        descricao="Desc",
        data_lancamento="2024-01-01",
        valor=10,
        tipo_lancamento="DES",
        situacao="PEND",
        id_usuario=1,
    )

    assert result is True
    assert mock_db_connection.commit.called


def test_buscar_lancamento_por_id(mock_db_connection, mocker):
    """
    Test finding a launch by ID.
    """
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchone.return_value = {"id": 5}
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor

    result = buscar_lancamento_por_id(5)
    assert result["id"] == 5
    args = mock_cursor.execute.call_args[0][1]
    assert args == (5,)


def test_atualizar_lancamento(mock_db_connection, mocker):
    """
    Test updating a launch.
    """
    mock_cursor = mocker.MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor

    result = atualizar_lancamento(
        launch_id=1,
        descricao="D",
        data_lancamento="2024",
        valor=5,
        tipo_lancamento="R",
        situacao="P",
        id_usuario=1,
    )

    assert result is True
    assert mock_db_connection.commit.called


def test_deletar_lancamento_db(mock_db_connection, mocker):
    """
    Test deleting a launch.
    """
    mock_cursor = mocker.MagicMock()
    mock_db_connection.cursor.return_value.__enter__.return_value = mock_cursor

    result = deletar_lancamento_db(1)

    assert result is True
    assert mock_db_connection.commit.called
    args = mock_cursor.execute.call_args[0][1]
    assert args == (1,)
