import mysql.connector
import os
from dotenv import load_dotenv
from dtos.errors import abort

load_dotenv()

db_config = {
    'host': 'localhost',
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn


def execute(query: str) -> list:
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute(query)
        conexion.commit()
        resultados = cursor.fetchall()

    except Exception as e:
        print(f"Error DB: {e}")
        abort(500, 'Error interno de base de datos')

    finally:
        cursor.close()
        conexion.close()

    return resultados
