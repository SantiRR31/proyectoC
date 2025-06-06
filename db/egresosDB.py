from db.conexion import conectar

# Funcion para buscar la descripcion de una clave en la tabla PARTIDAS_EGRESOS
def buscar_descripcion_db(clave):
    conn = conectar()
    if conn is None:
        return "Error de conexión"
    cursor = conn.cursor()
    cursor.execute('SELECT "DESCRIPCIÓN" FROM partidasEgresos WHERE "CLAVE CUCoP" = ?', (clave,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "No encontrada"

#

def buscar_clave_por_descripcion(descripcion):
    conn = conectar()
    if conn is None:
        return []
    cursor = conn.cursor()
    cursor.execute(
        'SELECT "CLAVE CUCoP", "DESCRIPCIÓN", "PARTIDA ESPECÍFICA" FROM partidasEgresos WHERE "DESCRIPCIÓN" LIKE ?',
        (f"%{descripcion}%",)
    )
    resultados = cursor.fetchall()
    conn.close()
    # Devuelve lista de diccionarios
    return [
        {"clave": fila[0], "descripcion": fila[1], "partida": fila[2]}
        for fila in resultados
    ]





def buscar_claves_por_texto(texto):
    conn = conectar()
    if conn is None:
        return []
    cursor = conn.cursor()
    cursor.execute('SELECT "CLAVE CUCoP", "DESCRIPCIÓN" FROM partidasEgresos WHERE "DESCRIPCIÓN" LIKE ?', (f"%{texto}%",))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
