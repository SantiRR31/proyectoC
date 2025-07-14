from datetime import datetime
import sqlite3
import os
import xlwings as xw
from utils.rutas import ruta_absoluta
from tkinter import messagebox

meses = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def confirmar_y_generar():
    respuesta = messagebox.askyesno("Generar reporte", "¿Está seguro de generar el reporte?")
    if respuesta:
        generar_reporte_xlwings()

def generar_reporte_xlwings():
    try:
        # Conectar con la base de datos
        conn = sqlite3.connect('prueba.db')
        cursor = conn.cursor()

        # Fecha actual y mes actual en formato YYYY-MM
        hoy = datetime.now()
        mes_actual = hoy.strftime('%Y-%m')
        nombre_hoja = hoy.strftime('%b %Y').lower()  # Ejemplo: 'may 2025'
        
        # Obtener pólizas del mes actual
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

        # Obtener claves únicas del mes actual
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

        # Abrir Excel
        app = xw.App(visible=False)
        wb = app.books.open(ruta_absoluta("assets/plantillaLibroIngresos.xls"))

        # Seleccionar hoja del mes
        try:
            sht = wb.sheets["feb 2025"]
        except:
            raise ValueError(f"No se encontró la hoja: '{nombre_hoja}' en el archivo Excel.")

        # Borrar datos anteriores en la hoja
        sht.range("A10:J40").clear_contents()
        
        mes_ano = f"{meses[hoy.month]}/{hoy.year}"
        sht.range("K5").value = mes_ano

        # Escribir encabezados de claves
        col_inicio = 4
        max_cols = 6
        columna_j = 10
        fila_formula = 41
        rango_inicio = 10
        rango_fin= 40
        
        num_claves = len(claves_mes)
        
        if num_claves > max_cols:
            col_a_insertar = num_claves - max_cols
            for offset in range (col_a_insertar):
                sht.range((1, columna_j)).api.EntireColumn.Insert()
                
                col_destino = columna_j + offset 
                letra_col = xw.utils.col_name(col_destino)
                
                formula = f"=SUMA({letra_col}{rango_inicio}:{letra_col}{rango_fin})"
                
                sht.range((fila_formula, col_destino)).formula = formula
                
        for idx, clave in enumerate(claves_mes):
            sht.range((8, col_inicio + idx)).value = clave

        # Escribir pólizas
        fila_inicio = 10
        for idx, (fecha, no_poliza, importe) in enumerate(polizas_mes):
            fila = fila_inicio + idx
            fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
            sht.range(f"A{fila}").value = fecha_dt
            sht.range(f"B{fila}").value = no_poliza
            sht.range(f"C{fila}").value = importe

            # Obtener abonos por clave
            cursor.execute("""
                SELECT clave, abono
                FROM detallePolizaIngreso
                WHERE noPoliza = ?
            """, (no_poliza,))
            abonos = dict(cursor.fetchall())

            # Escribir abonos
            for col_idx, clave in enumerate(claves_mes):
                sht.range((fila, col_inicio + col_idx)).value = abonos.get(clave, 0)

        # Guardar en carpeta personalizada
        carpeta_base = r"C:\Cecati122"
        carpeta_salida = os.path.join(carpeta_base, "InformesDeIngresos")
        os.makedirs(carpeta_salida, exist_ok=True)
        archivo_salida = os.path.join(carpeta_salida, f"ingresos_{mes_actual}.xlsx")
        
        mes_act = hoy.month
        anio_act = hoy.year
        nvo_nom_libro = f"{meses[mes_act]} {anio_act}"
        sht.name = nvo_nom_libro
                
        wb.save(archivo_salida)

        # Cerrar recursos
        wb.close()
        app.quit()
        conn.close()

        # Confirmación
        messagebox.showinfo("Reporte generado", f"El reporte se ha generado exitosamente:\n{archivo_salida}")
        return archivo_salida

    except Exception as e:
        print(f"Error generando el reporte: {e}")
        messagebox.showerror("Error", f"Ocurrió un error al generar el reporte:\n{e}")
