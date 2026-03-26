import os
import psycopg2
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados PostgreSQL
    usando as credenciais do arquivo .env.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
