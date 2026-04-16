from psycopg2.extras import RealDictCursor
from config.database import get_db_connection

def listar_lancamentos(id_usuario=None, data_filtro=None, situacao_filtro=None):
    """
    Acessa o banco de dados e lista os lançamentos com filtros opcionais.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = '''
                SELECT id, descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario
                FROM lancamento
                WHERE 1=1
            '''
            params = []
            
            if id_usuario:
                query += ' AND id_usuario = %s'
                params.append(id_usuario)
            if data_filtro:
                query += ' AND data_lancamento = %s'
                params.append(data_filtro)
            if situacao_filtro and situacao_filtro != 'ALL':
                query += ' AND situacao = %s'
                params.append(situacao_filtro)
                
            query += ' ORDER BY data_lancamento DESC'
            
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar lançamentos: {e}")
        return []
    finally:
        conn.close()

def inserir_lancamento(descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario):
    """
    Insere um novo lançamento no banco de dados.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = '''
                INSERT INTO lancamento (descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario))
            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao inserir lançamento: {e}")
        return False
    finally:
        conn.close()

def buscar_lancamento_por_id(id):
    """
    Busca um lançamento específico pelo seu ID.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = 'SELECT * FROM lancamento WHERE id = %s'
            cursor.execute(query, (id,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar lançamento por id: {e}")
        return None
    finally:
        conn.close()

def atualizar_lancamento(id, descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario):
    """
    Atualiza os dados de um lançamento existente.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = '''
                UPDATE lancamento 
                SET descricao = %s, data_lancamento = %s, valor = %s, tipo_lancamento = %s, situacao = %s, id_usuario = %s
                WHERE id = %s
            '''
            cursor.execute(query, (descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario, id))
            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao atualizar lançamento: {e}")
        return False
    finally:
        conn.close()

def deletar_lancamento_db(id):
    """
    Deleta um lançamento do banco de dados.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = 'DELETE FROM lancamento WHERE id = %s'
            cursor.execute(query, (id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao deletar lançamento: {e}")
        return False
    finally:
        conn.close()