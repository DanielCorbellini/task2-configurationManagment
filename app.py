import os
from flask import Flask, render_template, session, redirect, url_for, request
from services.lancamentos_service import listar_lancamentos, inserir_lancamento
from services.usuario_service import autenticar_usuario, listar_usuarios

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_SESSION_KEY")

@app.before_request
def require_login():
    allowed_routes = ['/login']
    if request.path not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('lancamento'))

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('lancamento'))
    
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('username')
    senha = request.form.get('password')
    
    usuario = autenticar_usuario(login, senha)
    
    if usuario:
        session['user_id'] = usuario['id']
        session['user_name'] = usuario['nome']
        return redirect(url_for('lancamento'))
    else:
        return render_template('login.html', error='Login ou senha inválidos')

@app.route('/lancamento')
def lancamento():
    lancamentos = listar_lancamentos()
    usuarios = listar_usuarios()
    return render_template('lancamento.html', lancamentos=lancamentos, usuarios=usuarios)

@app.route('/lancamento', methods=['POST'])
def lancamento_post():
    descricao = request.form.get('descricao')
    data_lancamento = request.form.get('data_lancamento')
    valor = request.form.get('valor')
    tipo_lancamento = request.form.get('tipo_lancamento')
    situacao = request.form.get('situacao')
    id_usuario = request.form.get('id_usuario') or session['user_id']
    
    inserir_lancamento(descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario)
    return redirect(url_for('lancamento'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug=True)