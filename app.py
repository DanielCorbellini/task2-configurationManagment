import os
from weasyprint import HTML
import io
from flask import send_file
from flask import Flask, render_template, session, redirect, url_for, request
from services.lancamentos_service import listar_lancamentos, inserir_lancamento
from services.usuario_service import autenticar_usuario, listar_usuarios

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_SESSION_KEY")

@app.before_request
def require_login():
    allowed_routes = ['login', 'login_post', 'static']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
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
    data_filtro = request.args.get('data')
    situacao_filtro = request.args.get('situacao')
    lancamentos = listar_lancamentos(id_usuario=session.get('user_id'), data_filtro=data_filtro, situacao_filtro=situacao_filtro)
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

@app.route('/exportar_pdf')
def exportar_pdf():    
    data_filtro = request.args.get('data')
    situacao_filtro = request.args.get('situacao')
    lancamentos = listar_lancamentos(id_usuario=session.get('user_id'), data_filtro=data_filtro, situacao_filtro=situacao_filtro)
    
    html_out = render_template('pdf_template.html', lancamentos=lancamentos)
    pdf_io = io.BytesIO()
    HTML(string=html_out).write_pdf(pdf_io)
    pdf_io.seek(0)
    
    return send_file(pdf_io, download_name='lancamentos.pdf', as_attachment=True, mimetype='application/pdf')

@app.route('/editar_lancamento/<int:id>', methods=['GET'])
def editar_lancamento(id):
    lancamento = listar_lancamentos(id)
    return render_template('editar_lancamento.html', lancamento=lancamento)

@app.route('/editar_lancamento/<int:id>', methods=['POST'])
def editar_lancamento_post(id):
    descricao = request.form.get('descricao')
    data_lancamento = request.form.get('data_lancamento')
    valor = request.form.get('valor')
    tipo_lancamento = request.form.get('tipo_lancamento')
    situacao = request.form.get('situacao')
    id_usuario = request.form.get('id_usuario') or session['user_id']
    
    editar_lancamento(id, descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario)
    return redirect(url_for('lancamento'))

@app.route('/deletar_lancamento/<int:id>', methods=['GET'])
def deletar_lancamento(id):
    deletar_lancamento(id)
    return redirect(url_for('lancamento'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
