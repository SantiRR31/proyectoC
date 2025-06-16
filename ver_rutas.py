import sqlite3
import xlwings as xw
from datetime import datetime
import os
import shutil

ruta_db = "prueba.db"
meses_esp = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
ruta_plantilla = "assets/plantillaAuxBancario.xls"
carpeta_destino = r"C:\Cecati122\Auxiliar Bancario"

def gen_aux_bancario(ruta_db, anio, mes):
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()
    
    os.makedirs(carpeta_destino, exist_ok=True)
    
    mes_str_1 = str(mes).zfill(2)
    
    nombre_archivo = f"auxiliar_bancario_{anio}-{mes_str_1}.xls"
    ruta_destino = os.path.join(carpeta_destino, nombre_archivo)
    
    shutil.copy(ruta_plantilla, ruta_destino)
    
    fecha_inicio = f"{anio}-{mes_str_1}-01"
    if mes == 12:
        fecha_fin = f"{anio + 1}-01-01"
    else:
        fecha_fin = f"{anio}-{str(mes + 1).zfill(2)}-01"
    
    query = """
    SELECT p.fecha, SUM(d.abono) as total_abono
    FROM detallePolizaIngreso d
    JOIN polizasIngresos p ON d.noPoliza = p.noPoliza
    WHERE substr(p.fecha, 7, 4) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2) >= ?
        AND substr(p.fecha, 7, 4) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2) < ?
    GROUP BY p.fecha
    ORDER BY substr(p.fecha, 7, 4) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2) ASC
    """
    cursor.execute(query, (fecha_inicio, fecha_fin))
    resultados = cursor.fetchall()
    
    conn.close()
    
    wb = xw.Book(ruta_destino)
    sht = wb.sheets[0]
    sht.name = "Aux Bancario"
    
    fecha_actual = datetime.now()
    mes_informado = f"{meses_esp[mes - 1]} {anio}"
    
    dia_str = fecha_actual.strftime("%d")
    mes_str_2 = fecha_actual.strftime("%m")
    anio_str = fecha_actual.strftime("%Y")
    
    sht.range("V4").value = mes_informado
    sht.range("AJ8").value = dia_str
    sht.range("AN8").value = mes_str_2
    sht.range("AS8").value = anio_str
    
    resultados = [
        (datetime.strptime(fecha, "%d/%m/%Y").date(), abono, "DEPÓSITO")
        for fecha, abono in resultados
    ]

    # Separar columnas
    fechas = [r[0] for r in resultados]
    conceptos = [r[2] for r in resultados]
    abonos = [r[1] for r in resultados]
    
    sht.range("B16").options(transpose=True).value = fechas
    sht.range("G16").options(transpose=True).value = conceptos
    sht.range("AF16").options(transpose=True).value = abonos
    
    
    #Guardar 
    wb.save(ruta_destino)
    wb.close()
    
    print("Archivo guardado como:", nombre_archivo)
    
gen_aux_bancario(ruta_db, 2025, 5)