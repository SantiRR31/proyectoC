from datetime import datetime
import sqlite3
import os
import xlwings as xw
from tkinter import messagebox

def confirmar_y_generar():
    respuesta = messagebox.askyesno("Generar reporte","¿Está seguro de generar el reporte?")
    if respuesta == True:
        generar_reporte_xlwings()

def generar_reporte_xlwings():
    try:
        conn = sqlite3.connect('prueba.db')
        cursor = conn.cursor()

        # Usar la fecha actual
        hoy = datetime.now()
        mes_actual = hoy.strftime('%Y-%m')

        # Obtener todas las pólizas del mes
        cursor.execute("""
            SELECT fecha, noPoliza, importe
            FROM polizasIngresos
            WHERE strftime('%Y-%m', 
                substr(fecha, 7) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2)
                ) = ?
        """, (mes_actual,))
        polizas_mes = cursor.fetchall()

        if not polizas_mes:
            raise ValueError("No se encontraron pólizas en el mes actual.")

        # Leer claves únicas del mes
        cursor.execute("""
            SELECT DISTINCT clave
            FROM detallePolizaIngreso d
            JOIN polizasIngresos p ON d.noPoliza = p.noPoliza
            WHERE strftime('%Y-%m', 
                substr(p.fecha, 7) || '-' || substr(p.fecha, 4, 2) || '-' || substr(p.fecha, 1, 2)
            ) = ?
            ORDER BY clave
        """, (mes_actual,))
        claves_mes = [row[0] for row in cursor.fetchall()]

        # Cargar plantilla y hoja
        app = xw.App(visible=False)
        wb = app.books.open("assets/plantillaLibroIngresos.xls")
        sht = wb.sheets['feb 2025']  # O cámbialo si varía por mes

        # Escribir datos generales de cada póliza
        fila_inicio = 10
        for idx, (fecha, no_poliza, importe) in enumerate(polizas_mes):
            sht.range(f"A{fila_inicio + idx}").value = fecha
            sht.range(f"B{fila_inicio + idx}").value = no_poliza
            sht.range(f"C{fila_inicio + idx}").value = importe

        # Escribir encabezados de claves
        col_inicio = 4
        #print("Escribiendo claves en encabezado:")
        #print("Claves obtenidas del mes:", claves_mes)
        for idx, clave in enumerate(claves_mes):
            celda = sht.range((8, col_inicio + idx))
            #print(f"Escribiendo clave '{clave}' en celda {celda.address}")
            celda.value = clave

        # Abonos por clave por cada póliza
        for idx, (_, no_poliza, _) in enumerate(polizas_mes):
            fila = fila_inicio + idx
            cursor.execute("""
                SELECT clave, abono
                FROM detallePolizaIngreso
                WHERE noPoliza = ?
            """, (no_poliza,))
            abonos = dict(cursor.fetchall())
            #print(f"Abonos de póliza {no_poliza}: {abonos}")
            for col_idx, clave in enumerate(claves_mes):
                valor = abonos.get(clave, 0)
                celda = sht.range((fila, col_inicio + col_idx))
                #print(f"  Poniendo valor {valor} en {celda.address}")
                celda.value = valor

        # Guardar el archivo
        carpeta_descargas = os.path.expanduser("~/Documentos/Cecati122/Reportes")
        os.makedirs(carpeta_descargas, exist_ok=True)
        archivo = os.path.join(carpeta_descargas, f"ingresos_{mes_actual}.xlsx")
        wb.save(archivo)
        wb.close()
        app.quit()
        conn.close()

        #print(f"Reporte generado: {archivo}")
        messagebox.showinfo("Reporte generado", f"El reporte se ha generado exitosamente:\n{archivo}")
        return archivo

    except Exception as e:
        print(f"Error generando el reporte: {e}")

