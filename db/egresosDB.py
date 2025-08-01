import sqlite3
from db.conexion import conectar
from models.egresomodelos import PolizaEgreso, ConceptoEgreso
from utils.utils import numero_a_letras_mxn

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
        SELECT 
            detalle."CLAVE CUCoP", 
            detalle."DESCRIPCIÓN", 
            detalle."PARTIDA ESPECÍFICA",
            partida."DESCRIPCIÓN"
        FROM partidasEgresos AS detalle
        JOIN partidasEgresos AS partida
            ON detalle."PARTIDA ESPECÍFICA" = partida."CLAVE CUCoP"
        WHERE detalle."DESCRIPCIÓN" LIKE ?
        UNION ALL
        SELECT 
            detalle."CLAVE CUCoP", 
            detalle."DESCRIPCIÓN", 
            detalle."PARTIDA ESPECÍFICA",
            partida."DESCRIPCIÓN"
        FROM partidasEgresos AS detalle
        JOIN partidasEgresos AS partida
            ON detalle."PARTIDA ESPECÍFICA" = partida."CLAVE CUCoP"
        WHERE detalle."DESCRIPCIÓN" LIKE ?
          AND detalle."DESCRIPCIÓN" NOT LIKE ?
        ''',
        (f"{descripcion}%", f"%{descripcion}%", f"{descripcion}%")
    )
    resultados = cursor.fetchall()
    conn.close()
    return [
        {
            "clave": fila[0],              # CUCoP
            "descripcion": fila[1],        # Desc del artículo
            "partida": fila[2],            # Clave partida
            "desc_partida": fila[3]        # Desc partida
        }
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
        return False, "Error de conexión o póliza vacía"

    cursor = conn.cursor()
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
                poliza.no_poliza,
                poliza.fecha,
                poliza.monto,
                poliza.nombre, 
                poliza.tipo_pago, 
                getattr(poliza, "clave_ref", None),
                poliza.denominacion, 
                poliza.observaciones,
                getattr(poliza, "no_cheque", None),
                poliza.estado or "activo"
            )
        )

        id_poliza = cursor.lastrowid

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
                (
                    id_poliza, 
                    concepto.clave_cucop, 
                    concepto.cargo,
                    concepto.partida_especifica
                )
            )

        conn.commit()
        return True, "Póliza y detalles insertados correctamente"
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if "UNIQUE constraint failed: polizasEgresos.no_poliza" in str(e):
            return False, f"Ya existe una póliza con el número '{poliza.no_poliza}'."
        return False, f"Error de integridad: {e}"
    except sqlite3.OperationalError as e:
        conn.rollback()
        return False, f"Error operativo: {e}"
    except Exception as e:
        conn.rollback()
        return False, f"Error inesperado: {e}"
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
        SELECT id_poliza, no_poliza, fecha, monto, nombre, tipo_pago, clave_ref, denominacion, observaciones, no_cheque, estado
        FROM polizasEgresos
        WHERE no_poliza = ?
        ''',
        (no_poliza,)
    )
    poliza_row = cursor.fetchone()
    if not poliza_row:
        conn.close()
        return None

    # Si la póliza está cancelada, se pone nombre = "Cancelado" y no se cargan conceptos
    estado = poliza_row[10]
    nombre = poliza_row[4]
    monto_letra = numero_a_letras_mxn(poliza_row[3]),
    
    if estado.lower() == "cancelado":
        nombre = "CANCELADO"
        monto_letra = "CANCELADO"
    
    # Crear el objeto PolizaEgreso
    poliza = PolizaEgreso(
        poliza_id=poliza_row[0],
        no_poliza=poliza_row[1],
        fecha=poliza_row[2],
        monto=poliza_row[3],
        monto_letra= monto_letra,
        nombre=nombre,
        tipo_pago=poliza_row[5],
        clave_ref=poliza_row[6],
        denominacion=poliza_row[7],
        observaciones=poliza_row[8],
        no_cheque=poliza_row[9],
        estado=estado
    )
    id_poliza = poliza_row[0]

    # Sólo cargar conceptos si no está cancelada
    if estado.lower() != "cancelado":
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
        ORDER BY CAST(SUBSTR(no_poliza, 1, INSTR(no_poliza, '/') - 1) AS INTEGER)
    """, (mes_actual,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_partidas_mes(mes_actual):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT d."CLAVE CUCoP"
        FROM detallePolizaEgreso d
        JOIN polizasEgresos p ON d.id_poliza = p.id_poliza
        WHERE strftime('%Y-%m', 
            substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)
        ) = ?
        ORDER BY d."CLAVE CUCoP"
    """, (mes_actual,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_conceptos_por_partida_especifica (id_poliza):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT "CLAVE CUCoP", SUM(cargo)
        FROM detallePolizaEgreso
        WHERE id_poliza = ?
        GROUP BY "CLAVE CUCoP"
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


def obtener_partidas_mesagrupasa(mes_actual): 
    conn = conectar()
    query = """
    SELECT d."CLAVE CUCoP", SUM(d.cargo)
    FROM detallePolizaEgreso d
    JOIN polizasEgresos po ON d.id_poliza = po.id_poliza
    WHERE strftime('%Y-%m', substr(po.fecha, 7) || '-' || substr(po.fecha, 4, 2) || '-' || substr(po.fecha, 1, 2)) = ?
      AND (po.estado IS NULL OR po.estado != 'cancelado')
    GROUP BY d."CLAVE CUCoP"
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

def cambiar_estado_poliza_id(id_poliza,nuevo_estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE polizasEgresos
        SET estado = ?
        WHERE id_poliza = ?
    ''', (nuevo_estado,id_poliza,))
    conn.commit()
    conn.close()

def obtener_polizas_egresos_filtrado(mes=None, anio=None):
    conn = conectar()
    cursor = conn.cursor()

    if mes and anio:
        cursor.execute('''
            SELECT id_poliza, no_poliza, fecha, nombre, monto, tipo_pago, estado
            FROM polizasEgresos
            WHERE SUBSTR(fecha, 4, 2) = ? AND SUBSTR(fecha, 7, 4) = ?
            ORDER BY CAST(SUBSTR(no_poliza, 1, 2) AS INTEGER) ASC
        ''', (f"{int(mes):02d}", str(anio)))
    else:
        cursor.execute('''
            SELECT id_poliza, no_poliza, fecha, nombre, monto, tipo_pago, estado
            FROM polizasEgresos
            ORDER BY CAST(SUBSTR(no_poliza, 1, 2) AS INTEGER) ASC
        ''')

    filas = cursor.fetchall()
    
    #print(f"DEBUG Pólizas filtradas ({mes}/{anio}): {filas}")

    conn.close()
    return filas


def obtener_poliza_completa(id_poliza):
    conn = conectar()
    cursor = conn.cursor()

    # Obtener datos de cabecera
    cursor.execute("""
        SELECT id_poliza, no_poliza,fecha, monto, nombre, tipo_pago,
               clave_ref, denominacion, observaciones, no_cheque, estado
        FROM polizasEgresos
        WHERE id_poliza = ?
    """, (id_poliza,))
    fila = cursor.fetchone()

    if not fila:
        return None

    poliza = PolizaEgreso(
        poliza_id=fila[0],
        no_poliza=fila[1],      
        fecha=fila[2],
        monto=fila[3], 
        nombre=fila[4],
        tipo_pago=fila[5],
        clave_ref=fila[6],
        denominacion=fila[7],
        observaciones=fila[8],
        no_cheque=fila[9],
        estado=fila[10]
    )

    # Obtener conceptos asociados
    cursor.execute("""
        SELECT d."CLAVE CUCoP", p.DESCRIPCIÓN, p."PARTIDA ESPECÍFICA", d.cargo
        FROM detallePolizaEgreso d
        JOIN partidasEgresos p ON d."CLAVE CUCoP" = p."CLAVE CUCoP"
        WHERE d.id_poliza = ?
    """, (id_poliza,))

    for concepto in cursor.fetchall():
        c = ConceptoEgreso(
            clave_cucop=concepto[0],
            descripcion=concepto[1],
            partida_especifica=concepto[2],
            cargo=concepto[3]
        )
        poliza.agregar_concepto(c)

    conn.close()
    return poliza


import sqlite3  # Asegúrate de tener este import

def actualizar_poliza(poliza: PolizaEgreso) -> tuple[bool, str]:
    print(f"Actualizando póliza: {poliza.no_poliza} (ID: {poliza.poliza_id})")

    conn = conectar()
    cursor = conn.cursor()
    try:
        if poliza.poliza_id:
            cursor.execute("""
                UPDATE polizasEgresos SET
                    no_poliza=?, fecha=?, monto=?, nombre=?, tipo_pago=?,
                    clave_ref=?, denominacion=?, observaciones=?, no_cheque=?
                WHERE id_poliza = ?
            """, (
                poliza.no_poliza, poliza.fecha, poliza.monto, poliza.nombre, poliza.tipo_pago,
                poliza.clave_ref, poliza.denominacion, poliza.observaciones,
                poliza.no_cheque, poliza.poliza_id
            ))

            cursor.execute("DELETE FROM detallePolizaEgreso WHERE id_poliza = ?", (poliza.poliza_id,))
            for concepto in poliza.conceptos:
                cursor.execute("""
                    INSERT INTO detallePolizaEgreso (id_poliza, "CLAVE CUCoP", "PARTIDA ESPECÍFICA", cargo)
                    VALUES (?, ?, ?, ?)
                """, (poliza.poliza_id, concepto.clave_cucop, concepto.partida_especifica, concepto.cargo))
        else:
            return False, "ID de póliza no proporcionado."

        conn.commit()
        return True, "Póliza actualizada correctamente."
    except sqlite3.IntegrityError as e:
        print("Error de integridad:", e)
        if "UNIQUE constraint failed: polizasEgresos.no_poliza" in str(e):
            return False, f"Ya existe una póliza con el número {poliza.no_poliza}. El número debe ser único."
        else:
            return False, f"Error de integridad: {e}"
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, f"Error inesperado al actualizar: {e}"
    finally:
        conn.close()

        
        
def eliminar_poliza(id_poliza: int):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys = ON")  # Activa FK para cascada
        cursor.execute("DELETE FROM polizasEgresos WHERE id_poliza = ?", (id_poliza,))
        conn.commit()
    except Exception as e:
        print("Error al eliminar póliza:", e)
    finally:
        conn.close()

def obtener_numeros_polizas_por_mes(mes: int, anio: int):
    conn = conectar()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    patron = f"%/{mes:02}/{anio}"
    
    cursor.execute(
        '''
        SELECT no_poliza
        FROM polizasEgresos
        WHERE fecha LIKE ?
        ORDER BY no_poliza
        ''',
        (patron,)
    )
    
    resultados = [fila[0] for fila in cursor.fetchall()]
    conn.close()
    return resultados
