import sqlite3

def conectar(nombre_db="db/prueba2.db"):
    """
    Crea y retorna una conexión a la base de datos SQLite.
    Por defecto se conecta a 'prueba.db'.
    """
    try:
        conn = sqlite3.connect(nombre_db)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
