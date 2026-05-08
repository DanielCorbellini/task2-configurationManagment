import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor
from config.database import get_db_connection


def buscar_usuario_por_login(login):
    """
    Searches for a user in the database by their login.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = "SELECT id, nome, login, situacao FROM usuario WHERE login = %s"
            cursor.execute(query, (login,))
            return cursor.fetchone()
    except psycopg2.Error as e:
        print(f"Erro ao buscar usuário: {e}")
        return None
    finally:
        conn.close()


def listar_usuarios():
    """
    Lists all users in the database.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = "SELECT id, nome FROM usuario"
            cursor.execute(query)
            return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Erro ao listar usuários: {e}")
        return []
    finally:
        conn.close()


def autenticar_usuario(login, senha):
    """
    Checks the user credentials.
    Generates the MD5 hash of the provided password and compares it
    with the password registered in the database.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = (
                "SELECT id, nome, login, senha, situacao FROM usuario WHERE login = %s"
            )
            cursor.execute(query, (login,))
            usuario = cursor.fetchone()

            if usuario:
                senha_hash = hashlib.md5(senha.encode("utf-8")).hexdigest()

                if usuario["senha"] == senha_hash:
                    # Removes the password hash from the returned object for security
                    del usuario["senha"]
                    return usuario

            return None
    except psycopg2.Error as e:
        print(f"Erro ao autenticar usuário: {e}")
        return None
    finally:
        conn.close()
