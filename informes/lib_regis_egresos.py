from datetime import datetime
from tkinter import messagebox, ttk
from db.egresosDB import obtener_conceptos_por_partida_especifica, obtener_partidas_mes, obtener_polizas_egresos_mes
from utils.config_utils import cargar_config
import customtkinter as ctk
from utils.egresos_utils import mostrar_loading_y_ejecutar
from utils.informes_utils import cerrar_recursos, eliminar_hoja_si_existe
from utils.rutas import ruta_absoluta
from utils.utils import obtener_nombre_hoja_desde_mes
import xlwings as xw
from widgets.widgets import ventana_seleccion_mes_anio_y_campos
import gc
import os

config = cargar_config()

meses = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def confirmar_y_generar_egresos(contenedor_principal=None):
    ventana_seleccion_mes_anio_y_campos(
        titulo="Generar reporte de egresos",
        funcion_generar=lambda mes_anio, vars_adicionales=None: mostrar_loading_y_ejecutar(
            lambda: generar_reporte_egresos_xlwings(mes_anio),
            contenedor_principal=contenedor_principal,
        ),
        contenedor_principal=contenedor_principal
    )

def generar_reporte_egresos_xlwings(mes_anio=None):
    app = None
    wb = None
    try:
        hoy = datetime.now()
        mes_actual = mes_anio if mes_anio else hoy.strftime('%Y-%m')
        anio, mes = mes_actual.split('-')
        mes_nombre = meses[int(mes)]
        nombre_hoja = obtener_nombre_hoja_desde_mes(mes_actual)

        polizas_mes = obtener_polizas_egresos_mes(mes_actual)
        if not polizas_mes:
            raise ValueError("No se encontraron pólizas de egresos en el mes actual.")

        partidas_mes = [row[0] for row in obtener_partidas_mes(mes_actual)]
        partidas_mes = ordenar_partidas(partidas_mes)

        app = xw.App(visible=False)
        wb = app.books.open(ruta_absoluta("assets/plantillas/LibroDeEgresos.xls"))
        eliminar_hoja_si_existe(wb, nombre_hoja)
        
        hoja_base = wb.sheets["mar 2025"]
        sht = hoja_base.copy(after=wb.sheets[-1])
        sht.name = nombre_hoja
        sht = wb.sheets[nombre_hoja]
        llenar_datos_generales(sht, mes_nombre, anio)

        ajustar_columnas(sht, partidas_mes)
        insertar_encabezados_partidas(sht, partidas_mes)
        insertar_filas_polizas(sht, polizas_mes, partidas_mes)
        archivo_salida = guardar_archivo(wb, mes_actual)

        mostrar_confirmacion()

        return archivo_salida

    except Exception as e:
        print(f"Error generando el reporte de egresos: {e}")
        messagebox.showerror("Error", f"Ocurrió un error al generar el reporte de egresos:\n{e}")

    finally:
        cerrar_recursos(wb, app)

def ordenar_partidas(partidas_mes):
    partidas_finales = [120, 330]
    partidas_ordenadas = sorted([p for p in partidas_mes if p not in partidas_finales])
    partidas_ordenadas += [p for p in partidas_finales if p in partidas_mes]
    return partidas_ordenadas


def llenar_datos_generales(sht, mes_nombre, anio):
    sht.range("T5").value = f"{mes_nombre} {anio}"
    sht.range("J5").value = config["no_cecati"]
    sht.range("AI5").value = config["clave_cecati"]
    sht.range("B5").value = config["estado"]


def ajustar_columnas(sht, partidas_mes):
    col_inicio = 4
    max_cols = 17
    columna_j = 10
    fila_formula = 47
    rango_inicio = 10
    rango_fin = 46

    num_partidas = len(partidas_mes)

    if num_partidas > max_cols:
        columnas_extra = num_partidas - max_cols
        for offset in range(columnas_extra):
            col_destino = columna_j + offset
            sht.range((1, col_destino)).api.EntireColumn.Insert()
            letra_col = xw.utils.col_name(col_destino)
            formula = f"=SUMA({letra_col}{rango_inicio}:{letra_col}{rango_fin})"
            sht.range((fila_formula, col_destino)).formula = formula

def insertar_encabezados_partidas(sht, partidas_mes):
    col_inicio = 4
    for idx, partida in enumerate(partidas_mes):
        sht.range((8, col_inicio + idx)).value = partida

def insertar_filas_polizas(sht, polizas_mes, partidas_mes):
    fila_inicio = 10
    rango_inicio = 10
    rango_fin = 46

    num_polizas = len(polizas_mes)

    if num_polizas > (rango_fin - rango_inicio + 1):
        filas_extra = num_polizas - (rango_fin - rango_inicio + 1)
        sht.range(f"A{rango_fin + 1}:A{rango_fin + filas_extra}").api.EntireRow.Insert()

    col_inicio = 4

    for idx, (fecha, no_poliza, id_poliza, tipo_pago, no_cheque, estado) in enumerate(polizas_mes):
        fila = fila_inicio + idx
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
        sht.range(f"A{fila}").value = fecha_dt
        sht.range(f"B{fila}").value = no_poliza.split("/")[0] if no_poliza else ""
        sht.range(f"C{fila}").value = no_cheque if tipo_pago == "CHEQUE" else "TRANS" if tipo_pago == "TRANSF. ELECTRÓNICA" else ""

        cargos = obtener_conceptos_por_partida_especifica(id_poliza)
        for col_idx, partida in enumerate(partidas_mes):
            if estado.lower() == "cancelado" and col_idx == 0:
                sht.range((fila, col_inicio + col_idx)).value = "cancelado"
            elif estado.lower() == "cancelado":
                sht.range((fila, col_inicio + col_idx)).value = ""
            else:
                valor = cargos.get(partida, 0)
                sht.range((fila, col_inicio + col_idx)).value = "" if valor == 0 else valor



def guardar_archivo(wb, mes_actual):
    carpeta_salida = os.path.join(config["carpeta_destino"], "InformesDeEgresos")
    os.makedirs(carpeta_salida, exist_ok=True)
    archivo_salida = os.path.join(carpeta_salida, f"egresos_{mes_actual}.xlsx")

    wb.app.calculation = 'automatic'
    wb.app.calculate()
    wb.save(archivo_salida)

    return archivo_salida


def mostrar_confirmacion():
    messagebox.showinfo(
        "Reporte generado",
        "El reporte de egresos se ha generado exitosamente.\n\nAtención:\nEl archivo fue generado. Si ves #### en las celdas, abre el archivo en Excel y presiona F9 o guarda el archivo para recalcular las fórmulas."
    )


    
    
    # función generar_reporte_egresos_
"""def generar_reporte_egresos_xlwings(mes_anio=None):
    app = None
    wb = None
    try:
        hoy = datetime.now()
        mes_actual = mes_anio if mes_anio else hoy.strftime('%Y-%m')
        nombre_hoja = hoy.strftime('%b %Y').lower()  # Ejemplo: 'jun 2025'

        polizas_mes = obtener_polizas_egresos_mes(mes_actual)
        if not polizas_mes:
            raise ValueError("No se encontraron pólizas de egresos en el mes actual.")

        partidas_mes = [row[0] for row in obtener_partidas_mes(mes_actual)]

        partidas_finales = [120, 330]
        # Filtra y ordena ascendente las demás
        partidas_ordenadas = sorted([p for p in partidas_mes if p not in partidas_finales])
        # Agrega al final las partidas especiales si existen en la lista
        partidas_ordenadas += [p for p in partidas_finales if p in partidas_mes]
        partidas_mes = partidas_ordenadas
        print(partidas_mes)

        # Abrir Excel de forma segura
        app = xw.App(visible=False)
        wb = app.books.open(ruta_absoluta("assets/plantillas/LibroDeEgresos.xls"))

        # Crear hoja si no existe
        nombre_hoja_plantilla = "mar 2025"
        if nombre_hoja not in [sheet.name.lower() for sheet in wb.sheets]:
            try:
                sht_plantilla = wb.sheets[nombre_hoja_plantilla]
                sht_nueva = sht_plantilla.copy(after=wb.sheets[-1])
                sht_nueva.name = nombre_hoja
            except Exception as e:
                raise ValueError(f"No se pudo crear la hoja '{nombre_hoja}': {e}")

        sht = wb.sheets[nombre_hoja]

        # Limpiar datos anteriores
        sht.range("A10:J40").clear_contents()

        # Encabezados
        mes_excel = hoy.strftime('%b-%y').lower()
        sht.range("T5").value = mes_excel
        sht.range("J5").value = config["no_cecati"]

        col_inicio = 4
        max_cols = 17
        columna_j = 10
        fila_formula = 47
        rango_inicio = 10
        rango_fin = 46

        num_partidas = len(partidas_mes)
        num_polizas = len(polizas_mes)

        # Insertar columnas si hay más partidas
        if num_partidas > max_cols:
            columnas_extra = num_partidas - max_cols
            for offset in range(columnas_extra):
                col_destino = columna_j + offset
                sht.range((1, col_destino)).api.EntireColumn.Insert()
                letra_col = xw.utils.col_name(col_destino)
                formula = f"=SUMA({letra_col}{rango_inicio}:{letra_col}{rango_fin})"
                sht.range((fila_formula, col_destino)).formula = formula

        # Escribir encabezados de partida
        for idx, partida in enumerate(partidas_mes):
            sht.range((8, col_inicio + idx)).value = partida

        # Insertar filas si hay más pólizas de las esperadas
        fila_inicio = 10
        if num_polizas > (rango_fin - rango_inicio + 1):
            filas_extra = num_polizas - (rango_fin - rango_inicio + 1)
            sht.range(f"A{rango_fin + 1}:A{rango_fin + filas_extra}").api.EntireRow.Insert()

        # Escribir datos de pólizas
        for idx, (fecha, no_poliza, id_poliza, tipo_pago, no_cheque, estado) in enumerate(polizas_mes):
            fila = fila_inicio + idx
            fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
            sht.range(f"A{fila}").value = fecha_dt
            sht.range(f"B{fila}").value = no_poliza.split("/")[0] if no_poliza else ""
            sht.range(f"C{fila}").value = no_cheque if tipo_pago == "CHEQUE" else "TRANS" if tipo_pago == "TRANSF. ELECTRÓNICA" else ""

            cargos = obtener_conceptos_por_partida_especifica(id_poliza)
            for col_idx, partida in enumerate(partidas_mes):
                if estado.lower() == "cancelado" and col_idx == 0:
                    # Solo en la primera columna de importes
                    sht.range((fila, col_inicio + col_idx)).value = "cancelado"
                elif estado.lower() == "cancelado":
                    # Las demás columnas quedan vacías
                    sht.range((fila, col_inicio + col_idx)).value = ""
                else:
                    valor = cargos.get(partida, 0)
                    sht.range((fila, col_inicio + col_idx)).value = "" if valor == 0 else valor

        # Guardar archivo en carpeta de salida
        carpeta_salida = os.path.join(config["carpeta_destino"], "InformesDeEgresos")
        os.makedirs(carpeta_salida, exist_ok=True)

        mes_act = hoy.month
        anio_act = hoy.year
        sht.name = f"{meses[mes_act]} {anio_act}"

        archivo_salida = os.path.join(carpeta_salida, f"egresos_{mes_actual}.xlsx")
        #app.visible = True
        wb.app.calculation = 'automatic'
        #sht.calculate()
        wb.app.calculate()
        wb.save(archivo_salida)

        # Confirmación
        
        messagebox.showinfo(
            "Reporte generado",
            "El reporte de egresos se ha generado exitosamente.\n\nAtención:\nEl archivo fue generado. Si ves #### en las celdas, abre el archivo en Excel y presiona F9 o guarda el archivo para recalcular las fórmulas."
        )

        return archivo_salida

    except Exception as e:
        print(f"Error generando el reporte de egresos: {e}")
        messagebox.showerror("Error", f"Ocurrió un error al generar el reporte de egresos:\n{e}")

    finally:
        # Limpieza segura de recursos
        try:
            if wb:
                
                wb.close()
        except Exception as e:
            print("Error cerrando el libro:", e)

        try:
            if app:
                app.quit()
        except Exception as e:
            print("Error cerrando Excel:", e)

        # Liberar memoria
        wb = None
        app = None
        sht = None
        
        gc.collect()"""
