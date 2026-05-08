import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """
    Creates and returns a connection to the PostgreSQL database
    using the credentials from the .env file.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )
