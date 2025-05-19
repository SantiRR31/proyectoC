import sqlite3


def buscar_denominacion_db(clave):
    conn = sqlite3.connect('prueba.db')
    cursor = conn.cursor()
    cursor.execute("SELECT denominacion FROM partidasIngresos WHERE partida = ?", (clave,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "No encontrada"

