import sqlite3
from db.conexion import conectar
from models.egresomodelos import PolizaEgreso, ConceptoEgreso

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
    try:
        cursor.execute(
            '''
            INSERT INTO polizasEgresos (
                "no_poliza",
                "fecha",
                "monto",
                "nombre",
                "tipo_pago",
                "clave_ref",
                "denominacion",
                "observaciones",
                "no_cheque",
                "estado"
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                poliza.poliza_id,
                poliza.fecha,
                poliza.monto,
                poliza.nombre, 
                poliza.tipo_pago, 
                getattr (poliza, "clave_ref", None),
                poliza.denominacion, 
                poliza.observaciones,
                getattr(poliza, "no_cheque", None),
                poliza.estado or "activo"
            )
        )
        # Obtener el id de la póliza recién insertada (si es autoincremental)
        id_poliza = cursor.lastrowid

        # Insertar los detalles (conceptos)
        for concepto in poliza.conceptos:
            cursor.execute(
                '''
                INSERT INTO detallePolizaEgreso (
                    id_poliza, 
                    "CLAVE CUCoP", 
                    cargo,
                    "PARTIDA ESPECÍFICA"
                ) VALUES (?, ?, ?, ?)
                ''',
                (id_poliza, 
                concepto.clave_cucop, 
                concepto.cargo,
                concepto.partida_especifica
                )
            )

        conn.commit()
        conn.close()
        return "Póliza y detalles insertados correctamente"
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE constraint failed: polizasEgresos.no_poliza" in str(e):
            return f"Ya existe una póliza con el número '{poliza.poliza_id}'."
        else:
            return f"Error de integridad: {str(e)}"    
    except sqlite3.OperationalError as e:
        conn.rollback()
        return f"Error operativo: {str(e)}"
    except Exception as e:
        conn.rollback()
        return f"Error inesperado: {str(e)}"
    finally:
        conn.close()

    
def obtener_siguiente_no_poliza_mes(fecha):
    """
    Devuelve el siguiente número de póliza para el mes y año de la fecha dada.
    fecha: string 'DD/MM/YYYY'
    """
    from datetime import datetime
    dt = datetime.strptime(fecha, "%d/%m/%Y")
    mes = dt.strftime("%m")
    anio = dt.strftime("%Y")
    conn = conectar()
    if conn is None:
        return "01"
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT COUNT(*) FROM polizasEgresos
        WHERE substr(fecha, 4, 2) = ? AND substr(fecha, 7, 4) = ?
        ''',
        (mes, anio)
    )
    resultado = cursor.fetchone()
    conn.close()
    consecutivo = (resultado[0] or 0) + 1
    return str(consecutivo).zfill(2)


def consultar_poliza_por_no(no_poliza):
    conn = conectar()
    if conn is None:
        return None
    cursor = conn.cursor()
    # 1. Consultar la póliza principal
    cursor.execute(
        '''
        SELECT id_poliza, no_poliza, fecha, monto, nombre, tipo_pago, clave_ref, denominacion, observaciones, no_cheque
        FROM polizasEgresos
        WHERE no_poliza = ?
        ''',
        (no_poliza,)
    )
    poliza_row = cursor.fetchone()
    if not poliza_row:
        conn.close()
        return None

    # Crear el objeto PolizaEgreso
    poliza = PolizaEgreso(
        poliza_id=poliza_row[1],   # no_poliza
        fecha=poliza_row[2],
        monto=poliza_row[3],
        montoletr="",  # Puedes calcularlo si lo necesitas
        nombre=poliza_row[4],
        tipo_pago=poliza_row[5],
        clave_ref=poliza_row[6],
        denominacion=poliza_row[7],
        observaciones=poliza_row[8],
        no_cheque=poliza_row[9],
        estado = poliza_row[10]
    )
    id_poliza = poliza_row[0]

    # 2. Consultar los conceptos (detalles)
    cursor.execute(
        '''
        SELECT "CLAVE CUCoP", cargo
        FROM detallePolizaEgreso
        WHERE id_poliza = ?
        ''',
        (id_poliza,)
    )
    detalles = cursor.fetchall()
    for detalle in detalles:
        clave_cucop = detalle[0]
        cargo = detalle[1]
        # Consultar descripción y partida_especifica si lo deseas
        cursor.execute(
            '''
            SELECT "DESCRIPCIÓN", "PARTIDA ESPECÍFICA"
            FROM partidasEgresos
            WHERE "CLAVE CUCoP" = ?
            ''',
            (clave_cucop,)
        )
        partida_row = cursor.fetchone()
        descripcion = partida_row[0] if partida_row else ""
        partida_especifica = partida_row[1] if partida_row else ""
        concepto = ConceptoEgreso(clave_cucop, descripcion, partida_especifica, cargo)
        poliza.agregar_concepto(concepto)
    conn.close()
    return poliza


def obtener_polizas_egresos_mes(mes_actual):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT fecha, no_poliza, id_poliza, tipo_pago, no_cheque, estado
        FROM polizasEgresos
        WHERE strftime('%Y-%m', 
            substr(fecha, 7) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)
        ) = ?
    """, (mes_actual,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_partidas_mes(mes_actual):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT d."PARTIDA ESPECÍFICA"
        FROM detallePolizaEgreso d
        JOIN polizasEgresos p ON d.id_poliza = p.id_poliza
        WHERE strftime('%Y-%m', 
            substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)
        ) = ?
        ORDER BY d."PARTIDA ESPECÍFICA"
    """, (mes_actual,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_conceptos_por_partida_especifica (id_poliza):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT "PARTIDA ESPECÍFICA", SUM(cargo)
        FROM detallePolizaEgreso
        WHERE id_poliza = ?
        GROUP BY "PARTIDA ESPECÍFICA"
    """, (id_poliza,))
    resultados = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in resultados}


def obtener_total_deudores(mes_anio):
    conn = conectar()
    query = """
    SELECT SUM(d.cargo)
    FROM detallePolizaEgreso d
    JOIN polizasEgresos p ON d.id_poliza = p.id_poliza
    WHERE d."PARTIDA ESPECÍFICA" = 120
      AND strftime('%Y-%m', 
          substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)
      ) = ?
    """
    cur = conn.cursor()
    cur.execute(query, (mes_anio,))
    result = cur.fetchone()
    return result[0] if result and result[0] is not None else 0

def obtener_total_acreedores(mes_anio):
    conn= conectar()
    query = """
    SELECT SUM(d.cargo)
    FROM detallePolizaEgreso d
    JOIN polizasEgresos p ON d.id_poliza = p.id_poliza
    WHERE d."PARTIDA ESPECÍFICA" = 330
      AND strftime('%Y-%m', 
          substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)
      ) = ?
    """
    cur = conn.cursor()
    cur.execute(query, (mes_anio,))
    result = cur.fetchone()
    return result[0] if result and result[0] is not None else 0


def agrupar_partidas_por_grupo(partidas_mes):
    grupos = {}
    for codigo, total_cargo in partidas_mes:
        codigo_str = str(codigo)
        if len(codigo_str) == 5:
            grupo = int(codigo_str[:2]) * 100
        elif len(codigo_str) == 4:
            grupo = int(codigo_str[:2]) * 100
        elif len(codigo_str) == 3:
            grupo = int(codigo_str[0]) * 100
        else:
            grupo = int(codigo)
        if grupo not in grupos:
            grupos[grupo] = []
        grupos[grupo].append((codigo, total_cargo))
    return grupos


def obtener_partidas_mesagrupasa (mes_actual): 
    conn = conectar()
    query = """
    SELECT d."PARTIDA ESPECÍFICA", SUM(d.cargo)
    FROM detallePolizaEgreso d
    JOIN polizasEgresos po ON d.id_poliza = po.id_poliza
    WHERE strftime('%Y-%m', substr(po.fecha, 7) || '-' || substr(po.fecha, 4, 2) || '-' || substr(po.fecha, 1, 2)) = ?
    GROUP BY d."PARTIDA ESPECÍFICA"
    """
    cur = conn.cursor()
    cur.execute(query, (mes_actual,))
    return cur.fetchall()


def obtener_polizas_egresos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_poliza, no_poliza, fecha, monto, nombre, estado
        FROM polizasEgresos
        ORDER BY fecha DESC
    ''')
    filas = cursor.fetchall()
    conn.close()
    return filas

def cancelar_poliza_por_id(id_poliza):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE polizasEgresos
        SET estado = 'cancelado'
        WHERE id_poliza = ?
    ''', (id_poliza,))
    conn.commit()
    conn.close()


def obtener_polizas_egresos_filtrado(mes=None, anio=None):
    conn = conectar()
    cursor = conn.cursor()

    if mes and anio:
        cursor.execute('''
            SELECT id_poliza, no_poliza, fecha, monto, nombre, estado
            FROM polizasEgresos
            WHERE strftime('%m', fecha) = ? AND strftime('%Y', fecha) = ?
            ORDER BY fecha DESC
        ''', (f"{int(mes):02d}", str(anio)))
    else:
        cursor.execute('''
            SELECT id_poliza, no_poliza, fecha, monto, nombre, estado
            FROM polizasEgresos
            ORDER BY fecha DESC
        ''')

    filas = cursor.fetchall()
    conn.close()
    return filas

