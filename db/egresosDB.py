from db.conexion import conectar

# Funcion para buscar la descripcion de una clave en la tabla PARTIDAS_EGRESOS
def buscar_descripcion_db(clave):
    conn = conectar()
    if conn is None:
        return "Error de conexión"
    cursor = conn.cursor()
    cursor.execute('SELECT "DESCRIPCIÓN" FROM PARTIDAS_EGRESOS WHERE "CLAVE CUCoP" = ?', (clave,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "No encontrada"

#
