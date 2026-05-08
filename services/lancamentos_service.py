import psycopg2
from psycopg2.extras import RealDictCursor
from config.database import get_db_connection


def listar_lancamentos(id_usuario=None, data_filtro=None, situacao_filtro=None):
    """
    Access the database and list the launches with optional filters.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT id, descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario
                FROM lancamento
                WHERE 1=1
            """
            params = []

            if id_usuario:
                query += " AND id_usuario = %s"
                params.append(id_usuario)
            if data_filtro:
                query += " AND data_lancamento = %s"
                params.append(data_filtro)
            if situacao_filtro and situacao_filtro != "ALL":
                query += " AND situacao = %s"
                params.append(situacao_filtro)

            query += " ORDER BY data_lancamento DESC"

            cursor.execute(query, tuple(params))
            return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Erro ao buscar lançamentos: {e}")
        return []
    finally:
        conn.close()


def inserir_lancamento(
    *,
    descricao,
    data_lancamento,
    valor,
    tipo_lancamento,
    situacao,
    id_usuario,
):
    """
    Inserts a new launch into the database.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                INSERT INTO lancamento (descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    descricao,
                    data_lancamento,
                    valor,
                    tipo_lancamento,
                    situacao,
                    id_usuario,
                ),
            )
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"Erro ao inserir lançamento: {e}")
        return False
    finally:
        conn.close()


def buscar_lancamento_por_id(launch_id):
    """
    Finds a specific launch by its ID.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = "SELECT * FROM lancamento WHERE id = %s"
            cursor.execute(query, (launch_id,))
            return cursor.fetchone()
    except psycopg2.Error as e:
        print(f"Erro ao buscar lançamento por id: {e}")
        return None
    finally:
        conn.close()


def atualizar_lancamento(
    *,
    launch_id,
    descricao,
    data_lancamento,
    valor,
    tipo_lancamento,
    situacao,
    id_usuario,
):
    """
    Updates the data of an existing launch.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = """
                UPDATE lancamento
                SET descricao = %s, data_lancamento = %s, valor = %s, tipo_lancamento = %s, situacao = %s, id_usuario = %s
                WHERE id = %s
            """
            cursor.execute(
                query,
                (
                    descricao,
                    data_lancamento,
                    valor,
                    tipo_lancamento,
                    situacao,
                    id_usuario,
                    launch_id,
                ),
            )
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"Erro ao atualizar lançamento: {e}")
        return False
    finally:
        conn.close()


def deletar_lancamento_db(launch_id):
    """
    Deletes a launch from the database.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM lancamento WHERE id = %s"
            cursor.execute(query, (launch_id,))
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"Erro ao deletar lançamento: {e}")
        return False
    finally:
        conn.close()
