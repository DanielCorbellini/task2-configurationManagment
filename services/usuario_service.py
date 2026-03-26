import hashlib
from psycopg2.extras import RealDictCursor
from config.database import get_db_connection

def buscar_usuario_por_login(login):
    """
    Busca um usuário no banco pelo seu login.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = "SELECT id, nome, login, situacao FROM usuario WHERE login = %s"
            cursor.execute(query, (login,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None
    finally:
        conn.close()

def autenticar_usuario(login, senha):
    """
    Verifica as credenciais do usuário.
    Gera o hash MD5 da senha fornecida e compara com a senha cadastrada no banco.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = "SELECT id, nome, login, senha, situacao FROM usuario WHERE login = %s"
            cursor.execute(query, (login,))
            usuario = cursor.fetchone()
            
            if usuario:
                senha_hash = hashlib.md5(senha.encode('utf-8')).hexdigest()
                
                if usuario['senha'] == senha_hash:
                    # Removemos o hash da senha do objeto retornado por segurança
                    del usuario['senha']
                    return usuario
                    
            return None
    except Exception as e:
        print(f"Erro ao autenticar usuário: {e}")
        return None
    finally:
        conn.close()
