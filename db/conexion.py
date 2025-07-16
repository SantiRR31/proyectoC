import sqlite3
from utils.rutas import ruta_absoluta

def conectar(nombre_db="db/prueba2.db"):
    """
    Crea y retorna una conexión a la base de datos SQLite.
    Por defecto se conecta a 'prueba.db'.
    """
    origen_db = ruta_absoluta(nombre_db)
    try:
        conn = sqlite3.connect(origen_db)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def conectar_db(nombre_db="prueba.db"):
    """
    Conecta a la base de datos y retorna la conexión.
    Si no se puede conectar, retorna None.
    """
    conn = conectar(nombre_db)
    if conn is None:
        print("No se pudo establecer la conexión a la base de datos.")
    return conn
