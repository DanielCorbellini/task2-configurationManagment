import io
import os
from flask import Flask, redirect, render_template, request, send_file, session, url_for
from weasyprint import HTML
from services.lancamentos_service import (
    atualizar_lancamento,
    buscar_lancamento_por_id,
    deletar_lancamento_db,
    inserir_lancamento,
    listar_lancamentos,
)
from services.usuario_service import autenticar_usuario, listar_usuarios

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_SESSION_KEY")


@app.before_request
def require_login():
    """
    Checks if the user is authenticated before accessing any route.
    """
    allowed_routes = ["login", "login_post", "static"]

    if request.endpoint not in allowed_routes and "user_id" not in session:
        return redirect(url_for("login"))

    return None


@app.route("/")
def index():
    """
    Redirects to the main page.
    """
    return redirect(url_for("lancamento"))


@app.route("/login")
def login():
    """
    Handles the login page GET request.
    """
    if "user_id" in session:
        return redirect(url_for("lancamento"))

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    """
    Handles the login page POST request.
    """
    user_login = request.form.get("username")
    user_password = request.form.get("password")

    usuario = autenticar_usuario(user_login, user_password)

    if usuario:
        session["user_id"] = usuario["id"]
        session["user_name"] = usuario["nome"]

        return redirect(url_for("lancamento"))

    return render_template("login.html", error="Login ou senha inválidos")


@app.route("/lancamento")
def lancamento():
    """
    Handles the main dashboard page GET request.
    """
    data_filtro = request.args.get("data")
    situacao_filtro = request.args.get("situacao")
    lancamentos = listar_lancamentos(
        id_usuario=session.get("user_id"),
        data_filtro=data_filtro,
        situacao_filtro=situacao_filtro,
    )
    usuarios = listar_usuarios()

    return render_template(
        "lancamento.html", lancamentos=lancamentos, usuarios=usuarios
    )


@app.route("/lancamento", methods=["POST"])
def lancamento_post():
    """
    Handles the main dashboard page POST request.
    """
    descricao = request.form.get("descricao")
    data_lancamento = request.form.get("data_lancamento")
    valor = request.form.get("valor")
    tipo_lancamento = request.form.get("tipo_lancamento")
    situacao = request.form.get("situacao")
    id_usuario = request.form.get("id_usuario") or session["user_id"]

    inserir_lancamento(
        descricao=descricao,
        data_lancamento=data_lancamento,
        valor=valor,
        tipo_lancamento=tipo_lancamento,
        situacao=situacao,
        id_usuario=id_usuario,
    )

    return redirect(url_for("lancamento"))


@app.route("/logout")
def logout():
    """
    Handles the logout request.
    """
    session.pop("user_id", None)
    session.pop("user_name", None)

    return redirect(url_for("login"))


@app.route("/exportar_pdf")
def exportar_pdf():
    """
    Handles the PDF export request.
    """
    data_filtro = request.args.get("data")
    situacao_filtro = request.args.get("situacao")
    lancamentos = listar_lancamentos(
        id_usuario=session.get("user_id"),
        data_filtro=data_filtro,
        situacao_filtro=situacao_filtro,
    )

    html_out = render_template("pdf_template.html", lancamentos=lancamentos)
    pdf_io = io.BytesIO()
    HTML(string=html_out).write_pdf(pdf_io)
    pdf_io.seek(0)

    return send_file(
        pdf_io,
        download_name="lancamentos.pdf",
        as_attachment=True,
        mimetype="application/pdf",
    )


@app.route("/editar_lancamento/<int:id>", methods=["GET"])
def editar_lancamento_route(launch_id):
    """
    Handles the edit launch page GET request.
    """
    edit_lancamento = buscar_lancamento_por_id(launch_id)
    # Render the main dashboard but pass edit_lancamento so the modal can trigger
    data_filtro = request.args.get("data")
    situacao_filtro = request.args.get("situacao")
    lancamentos = listar_lancamentos(
        id_usuario=session.get("user_id"),
        data_filtro=data_filtro,
        situacao_filtro=situacao_filtro,
    )
    usuarios = listar_usuarios()

    return render_template(
        "lancamento.html",
        lancamentos=lancamentos,
        usuarios=usuarios,
        edit_lancamento=edit_lancamento,
    )


@app.route("/editar_lancamento/<int:id>", methods=["POST"])
def editar_lancamento_post(launch_id):
    """
    Handles the edit launch page POST request.
    """
    descricao = request.form.get("descricao")
    data_lancamento = request.form.get("data_lancamento")
    valor = request.form.get("valor")
    tipo_lancamento = request.form.get("tipo_lancamento")
    situacao = request.form.get("situacao")
    id_usuario = request.form.get("id_usuario") or session["user_id"]

    atualizar_lancamento(
        launch_id=launch_id,
        descricao=descricao,
        data_lancamento=data_lancamento,
        valor=valor,
        tipo_lancamento=tipo_lancamento,
        situacao=situacao,
        id_usuario=id_usuario,
    )

    return redirect(url_for("lancamento"))


@app.route("/deletar_lancamento/<int:id>", methods=["GET"])
def deletar_lancamento_route(launch_id):
    """
    Handles the delete launch page GET request.
    """
    deletar_lancamento_db(launch_id)
    return redirect(url_for("lancamento"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
