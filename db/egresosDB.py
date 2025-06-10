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

""" def buscar_clave_por_descripcion(descripcion):
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
    ] """
    
def buscar_clave_por_descripcion(descripcion):
    conn = conectar()
    if conn is None:
        return []
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT "CLAVE CUCoP", "DESCRIPCIÓN", "PARTIDA ESPECÍFICA"
        FROM partidasEgresos
        WHERE "DESCRIPCIÓN" LIKE ?
        UNION ALL
        SELECT "CLAVE CUCoP", "DESCRIPCIÓN", "PARTIDA ESPECÍFICA"
        FROM partidasEgresos
        WHERE "DESCRIPCIÓN" LIKE ? AND "DESCRIPCIÓN" NOT LIKE ?
        ''',
        (f"{descripcion}%", f"%{descripcion}%", f"{descripcion}%")
    )
    resultados = cursor.fetchall()
    conn.close()
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


def obtener_partida_especifica_por_clave(clave_cucop):
    conn = conectar()
    if conn is None:
        return ""
    cursor = conn.cursor()
    cursor.execute(
        'SELECT "PARTIDA ESPECÍFICA" FROM partidasEgresos WHERE "CLAVE CUCoP" = ?',
        (clave_cucop,)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else ""

def inrtar_poliza_egreso(poliza):
    conn = conectar()
    if conn is None or not poliza:
        return "Error de conexion o poliza vacia"
    cursor = conn.cursor()
    # Insertar la póliza principal
    cursor.execute(
        '''
        INSERT INTO polizasEgresos (
            "FECHA", "NO. DE PÓLIZA", "NOMBRE", "MONTO", "MONTO EN LETRAS",
            "TIPO DE PAGO", "CLAVE DE RASTREO", "DENOMINACIÓN", "OBSERVACIONES"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            poliza.fecha, poliza.poliza_id, poliza.nombre, poliza.monto,
            poliza.montoletr, poliza.tipo_pago, poliza.clave_ref,
            poliza.denominacion, poliza.observaciones
        )
    )
    # Obtener el id de la póliza recién insertada (si es autoincremental)
    id_poliza = cursor.lastrowid

    # Insertar los detalles (conceptos)
    for concepto in poliza.conceptos:
        cursor.execute(
            '''
            INSERT INTO detallePolizaEgreso (
                id_poliza, "CLAVE CUCoP", cargo
            ) VALUES (?, ?, ?)
            ''',
            (id_poliza, concepto.clave_cucop, concepto.cargo)
        )

    conn.commit()
    conn.close()
    return "Póliza y detalles insertados correctamente"
    