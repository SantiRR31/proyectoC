import sqlite3
from db.conexion import conectar, conectar_db
import sqlite3


# ---- Auxiliar deudores diversos ----

def obtener_partidas_120_por_mes(mes_anio):
    # mes_anio debe ser 'YYYY-MM'
    conn = conectar()
    cursor = conn.cursor()
    query = """
        SELECT d.cargo, p.fecha, p.nombre, p.no_poliza
        FROM detallePolizaEgreso d
        JOIN polizasEgresos p ON d.id_poliza = p.id_poliza
        WHERE d."PARTIDA ESPECÍFICA" = 120
          AND strftime('%Y-%m', substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)) = ?
          AND estado != "cancelado"
    """
    cursor.execute(query, (mes_anio,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
  
def obtener_partidas_i_120_por_mes(mes_anio):
  conn = conectar_db()
  cursor = conn.cursor()
  query = """
        SELECT  pi.importe as cargo , pi.fecha 
        from polizasIngresos pi
        where exists (
        SELECT 1
        FROM detallePolizaIngreso dpi
        WHERE dpi.noPoliza = pi.noPoliza
          AND dpi.clave = 120
    )
      AND strftime('%Y-%m', substr(pi.fecha, 7) || '-' || substr(pi.fecha, 4, 2) || '-' || substr(pi.fecha, 1, 2)) = ?;
      """
  cursor.execute(query, (mes_anio,))
  resultados = cursor.fetchall()
  conn.close()
  return resultados

def obtener_partidas_e_330_mes(mes_anio):
    # mes_anio debe ser 'YYYY-MM'
    conn = conectar()
    cursor = conn.cursor()
    query = """
        SELECT d.cargo, p.fecha
        FROM detallePolizaEgreso d
        JOIN polizasEgresos p ON d.id_poliza = p.id_poliza
        WHERE d."PARTIDA ESPECÍFICA" = 330
          AND strftime('%Y-%m', substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)) = ?
          AND estado != "cancelado"
    """
    cursor.execute(query, (mes_anio,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
  
def obtener_partidas_i_330_mes(mes_anio):
  conn = conectar_db()
  cursor = conn.cursor()
  query = """
        SELECT  pi.importe as cargo , pi.fecha 
        from polizasIngresos pi
        where exists (
        SELECT 1
        FROM detallePolizaIngreso dpi
        WHERE dpi.noPoliza = pi.noPoliza
          AND dpi.clave = 330
    )
      AND strftime('%Y-%m', substr(pi.fecha, 7) || '-' || substr(pi.fecha, 4, 2) || '-' || substr(pi.fecha, 1, 2)) = ?;
      """
  cursor.execute(query, (mes_anio,))
  resultados = cursor.fetchall()
  conn.close()
  return resultados


def obte_poliz_egre(mes_anio):
  conn = conectar()
  cursor = conn.cursor()
  query ="""
    SELECT 
        p.fecha,
        p.nombre,
        p.tipo_pago,
        p.no_cheque,
        p.monto
    FROM polizasEgresos p
    WHERE strftime('%Y-%m', 
        substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)
    ) = ?;
    """
  cursor.execute(query, (mes_anio,))
  resultados = cursor.fetchall()
  conn.close()
  return resultados

def obte_poliz_ingre(mes_anio):
  conn = conectar_db()
  cursor = conn.cursor()
  query = """
    SELECT p.fecha, SUM(d.abono) as total_abono
    FROM detallePolizaIngreso d
    JOIN polizasIngresos p ON d.noPoliza = p.noPoliza
    WHERE substr(p.fecha, 7, 4) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2) >= ?
        AND substr(p.fecha, 7, 4) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2) < ?
    """
  cursor.execute(query, (mes_anio, mes_anio))
  resultados = cursor.fetchall()
  conn.close()
  return resultados