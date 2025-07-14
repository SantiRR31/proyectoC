from datetime import datetime
from tkinter import messagebox, ttk
from db.egresosDB import obtener_conceptos_por_partida_especifica, obtener_partidas_mes, obtener_polizas_egresos_mes
from utils.config_utils import cargar_config
import customtkinter as ctk
from utils.egresos_utils import mostrar_loading_y_ejecutar
import xlwings as xw
import gc
import os

config = cargar_config()


meses = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def confirmar_y_generar_egresos(contenedor_principal=None):
    ventana = ctk.CTkToplevel()
    ventana.title("Generar reporte de egresos")
    ventana.geometry("340x180")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.transient(contenedor_principal)

    meses_lista = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    hoy = datetime.now()
    mes_actual = hoy.month
    anio_actual = hoy.year

    ctk.CTkLabel(ventana, text="Seleccione el mes y año del reporte:", font=("Arial", 13)).pack(pady=(16, 6))

    frame = ctk.CTkFrame(ventana, fg_color="transparent")
    frame.pack(pady=4)

    mes_var = ctk.StringVar(value=meses_lista[mes_actual-1])
    anio_var = ctk.StringVar(value=str(anio_actual))

    mes_cb = ttk.Combobox(frame, values=meses_lista, textvariable=mes_var, state="readonly", width=14)
    mes_cb.grid(row=0, column=0, padx=8)
    anio_cb = ttk.Combobox(frame, values=[str(a) for a in range(anio_actual-5, anio_actual+2)], textvariable=anio_var, width=8, state="readonly")
    anio_cb.grid(row=0, column=1, padx=8)

    def generar_reporte_seleccionado():
        mes_idx = meses_lista.index(mes_var.get()) + 1
        anio = int(anio_var.get())
        mes_str = f"{anio}-{mes_idx:02d}"
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            lambda: generar_reporte_egresos_xlwings(mes_str),
            contenedor_principal=contenedor_principal,
        )

    def generar_reporte_actual():
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            generar_reporte_egresos_xlwings,
            contenedor_principal=contenedor_principal,
        )

    btn_frame = ctk.CTkFrame(ventana, fg_color="transparent")
    btn_frame.pack(pady=18)

    ctk.CTkButton(btn_frame, text="Generar mes seleccionado", command=generar_reporte_seleccionado, width=140).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Generar mes actual", command=generar_reporte_actual, width=120).pack(side="left", padx=10)

# función generar_reporte_egresos_
def generar_reporte_egresos_xlwings(mes_anio=None):
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
        wb = app.books.open("assets/plantillas/LibroDeEgresos.xls")

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
        for idx, (fecha, no_poliza, id_poliza, tipo_pago, no_cheque) in enumerate(polizas_mes):
            fila = fila_inicio + idx
            fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
            sht.range(f"A{fila}").value = fecha_dt
            sht.range(f"B{fila}").value = no_poliza.split("/")[0] if no_poliza else ""
            sht.range(f"C{fila}").value = no_cheque if tipo_pago == "CHEQUE" else "TRANS" if tipo_pago == "TRANSF. ELECTRÓNICA" else ""

            cargos = obtener_conceptos_por_partida_especifica(id_poliza)
            for col_idx, partida in enumerate(partidas_mes):
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
        
        gc.collect()
