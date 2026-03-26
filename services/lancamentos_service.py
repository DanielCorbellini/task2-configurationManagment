from psycopg2.extras import RealDictCursor
from config.database import get_db_connection

def listar_lancamentos(id_usuario=None):
    """
    Acessa o banco de dados e lista os lançamentos.
    Se id_usuario for fornecido, filtra apenas os lançamentos desse usuário.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            if id_usuario:
                query = '''
                    SELECT id, descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario
                    FROM lancamento
                    WHERE id_usuario = %s
                    ORDER BY data_lancamento DESC
                '''
                cursor.execute(query, (id_usuario,))
            else:
                query = '''
                    SELECT id, descricao, data_lancamento, valor, tipo_lancamento, situacao, id_usuario
                    FROM lancamento
                    ORDER BY data_lancamento DESC
                '''
                cursor.execute(query)
            
            resultados = cursor.fetchall()
            return resultados
    except Exception as e:
        print(f"Erro ao buscar lançamentos: {e}")
        return []
    finally:
        conn.close()
