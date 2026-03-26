from flask import Flask, render_template, session, redirect, url_for, request
from services.lancamentos_service import listar_lancamentos

app = Flask(__name__)

@app.before_request
def require_login():
    allowed_routes = ['/', 'login']
    if request.path not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('lancamento'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/lancamento')
def lancamento():
    lancamentos = listar_lancamentos()
    return render_template('lancamento.html', lancamentos=lancamentos)


if __name__ == '__main__':
    app.run(debug=True)