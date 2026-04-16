import pytest
from flask import session

def test_login_page_renders_200(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'ConfigFinance | Entrar' in response.data

def test_login_post_success(client, mocker):
    mocker.patch('app.autenticar_usuario', return_value={'id': 1, 'nome': 'Admin'})
    response = client.post('/login', data={'username': 'admin', 'password': '123'})
    assert response.status_code == 302
    with client.session_transaction() as sess:
        assert sess['user_id'] == 1

def test_login_post_failure(client, mocker):
    mocker.patch('app.autenticar_usuario', return_value=None)
    response = client.post('/login', data={'username': 'admin', 'password': 'wrong'})
    assert response.status_code == 200
    assert b'Login ou senha' in response.data

def test_logout_clears_session(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['user_name'] = 'Admin'
    response = client.get('/logout')
    assert response.status_code == 302
    with client.session_transaction() as sess:
        assert 'user_id' not in sess

def test_firewall_blocks_unauthenticated(client):
    response = client.get('/lancamento')
    assert response.status_code == 302
    assert '/login' in response.headers.get('Location', '') or b'/login' in response.data

def test_firewall_allows_static(client):
    response = client.get('/static/style.css')
    assert response.status_code != 302

def test_lancamento_page_renders(client, mocker):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mocker.patch('app.listar_lancamentos', return_value=[])
    mocker.patch('app.listar_usuarios', return_value=[])
    response = client.get('/lancamento')
    assert response.status_code == 200

def test_lancamento_page_filters(client, mocker):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mock_list = mocker.patch('app.listar_lancamentos', return_value=[])
    mocker.patch('app.listar_usuarios', return_value=[])
    response = client.get('/lancamento?data=2024-01-01&situacao=PENDENTE')
    assert response.status_code == 200
    mock_list.assert_called_once_with(id_usuario=1, data_filtro='2024-01-01', situacao_filtro='PENDENTE')

def test_lancamento_post_creates_and_redirects(client, mocker):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mock_inserir = mocker.patch('app.inserir_lancamento')
    response = client.post('/lancamento', data={
        'descricao': 'Test',
        'data_lancamento': '2024-01-01',
        'valor': '10.50',
        'tipo_lancamento': 'DESPESA',
        'situacao': 'EFETIVADO',
        'id_usuario': 1
    })
    assert response.status_code == 302
    mock_inserir.assert_called_once()

def test_exportar_pdf_renders(client, mocker):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mocker.patch('app.listar_lancamentos', return_value=[])
    mocker.patch('app.HTML.write_pdf')
    response = client.get('/exportar_pdf')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/pdf'

def test_editar_lancamento_route_modal(client, mocker):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mocker.patch('app.buscar_lancamento_por_id', return_value={'id': 1, 'descricao': 'EDIT_ME'})
    mocker.patch('app.listar_lancamentos', return_value=[])
    mocker.patch('app.listar_usuarios', return_value=[])
    response = client.get('/editar_lancamento/1')
    assert response.status_code == 200
    assert b'EDIT_ME' in response.data

def test_editar_lancamento_post_saves(client, mocker):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mock_atualizar = mocker.patch('app.atualizar_lancamento')
    response = client.post('/editar_lancamento/1', data={
        'descricao': 'Updated',
        'data_lancamento': '2024-01-01',
        'valor': '20.00',
        'tipo_lancamento': 'RECEITA',
        'situacao': 'PENDENTE',
        'id_usuario': 1
    })
    assert response.status_code == 302
    mock_atualizar.assert_called_once()

def test_deletar_lancamento_redirects(client, mocker):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mock_del = mocker.patch('app.deletar_lancamento_db')
    response = client.get('/deletar_lancamento/1')
    assert response.status_code == 302
    mock_del.assert_called_once_with(1)
