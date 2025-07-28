from datetime import datetime
from tkinter import messagebox, ttk
import customtkinter as ctk
from db.egresosDB import agrupar_partidas_por_grupo, obtener_partidas_mesagrupasa, obtener_total_acreedores, obtener_total_deudores
from utils.config_utils import cargar_config
from utils.egresos_utils import mostrar_loading_y_ejecutar
import os
import gc
from utils.rutas import ruta_absoluta
import xlwings as xw
import re

config = cargar_config()

meses = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def confirmar_y_generar_consolidado(contenedor_principal=None):
    ventana = ctk.CTkToplevel()
    ventana.title("Generar informe consolidado de egresos")
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
            lambda: generar_informe_consolidado_egresos(mes_str),
            contenedor_principal=contenedor_principal,
        )

    def generar_reporte_actual():
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            generar_informe_consolidado_egresos,
            contenedor_principal=contenedor_principal,
        )

    btn_frame = ctk.CTkFrame(ventana, fg_color="transparent")
    btn_frame.pack(pady=18)

    ctk.CTkButton(btn_frame, text="Generar mes seleccionado", command=generar_reporte_seleccionado, width=140).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Generar mes actual", command=generar_reporte_actual, width=120).pack(side="left", padx=10)



def generar_informe_consolidado_egresos(mes_anio=None):
    app = None
    wb = None
    try:
        hoy = datetime.now()
        mes_actual = mes_anio if mes_anio else hoy.strftime('%Y-%m')
        # Extrae año y mes del string 'YYYY-MM'
        anio, mes = mes_actual.split('-')
        mes_nombre = meses[int(mes)]
        partidas_mes = obtener_partidas_mesagrupasa(mes_actual)  # Debe devolver (codigo, descripcion, total_cargo)
        
        # Abrir plantilla
        app = xw.App(visible=False)
        wb = app.books.open(ruta_absoluta("assets/plantillas/ConsolidadoEgresos.xls"))
        sht = wb.sheets[0]  # O el nombre de la hoja

        # Llenar datos generales
        sht.range("M5").value = f"CECATI No. {config['no_cecati']}"
        sht.range("R8").value = f"{mes_nombre} {anio}"
        sht.range("AH8").value = hoy.strftime("%d %m %Y")

        # Diccionario de rangos por grupo
        rangos = {
            2100: ("C14", "C20"),
            2200: ("C24", "C25"),
            2400: ("C29", "C37"),
            2500: ("C41", "C45"),
            2600: ("C49", "C51"),
            2700: ("C54", "C58"),
            2900: ("C61", "C67"),
            3100: ("R14", "R20"),
            3200: ("R23", "R23"),
            3300: ("R27", "R33"),
            3400: ("R37", "R40"),
            3500: ("R45", "R52"),
            3600: ("R55", "R55"),
            3700: ("R58", "R64"),
            3800: ("R67", "R69"),
            3900: ("R73", "R73"),
            4400: ("AG14", "AG15"),
            5100: ("AG22", "AG25"),
            5200: ("AG29", "AG32"),
            5300: ("AG36", "AG37"),
            5600: ("AG40", "AG44"),
            5900: ("AG48", "AG48"),
        }
        
        columnas_cargo = {
            2100: "H",
            2200: "H",
            2400: "H",
            2500: "H",
            2600: "H",
            2700: "H",
            2900: "H",
            3100: "W",
            3200: "W",
            3300: "W",
            3400: "W",
            3500: "W",
            3600: "W",
            3700: "W",
            3800: "W",
            3900: "W",
            4400: "AL",
            5100: "AL",
            5200: "AL",
            5300: "AL",
            5600: "AL",
            5900: "AL",
        }
        
        # Otros
        sht.range("Al59").value = obtener_total_deudores(mes_actual)
        sht.range("Al60").value = obtener_total_acreedores(mes_actual)

        # Agrupa partidas por grupo (2100, 2200, etc.)
        partidas_por_grupo = agrupar_partidas_por_grupo(partidas_mes)
        
        #print("Partidas por grupo:", partidas_por_grupo)
        
        carpeta_salida = os.path.join(config["carpeta_destino"], "Consolidado de egresos")
        os.makedirs(carpeta_salida, exist_ok=True)

        # Para cada grupo, coloca los códigos y cargos en las celdas correspondientes

        for grupo, (inicio, fin) in rangos.items():
            codigos = partidas_por_grupo.get(grupo, [])
            col = re.match(r'[A-Z]+', inicio).group()
            fila_inicio = int(re.search(r'\d+', inicio).group())
            col_cargo = columnas_cargo[grupo]
            for i, (codigo, total_cargo) in enumerate(codigos):
                if fila_inicio + i > int(re.search(r'\d+', fin).group()):
                    break
                celda_codigo = f"{col}{fila_inicio + i}"
                celda_cargo = f"{col_cargo}{fila_inicio + i}"
                try:
                    sht.range(celda_codigo).value = codigo
                    sht.range(celda_cargo).value = total_cargo
                except Exception as e:
                    print(f"Error al escribir en {celda_codigo} o {celda_cargo}: {e}")
                    raise
                
        # Guardar archivo
        archivo_salida = os.path.join(carpeta_salida, f"consolidado_egresos_{mes_actual}_{anio}.xlsx")
        wb.save(archivo_salida)
        messagebox.showinfo("Reporte generado", f"El informe consolidado se ha generado:\n{archivo_salida}")
        return archivo_salida

    except Exception as e:
        print(f"Error generando el informe consolidado: {e}")
        messagebox.showerror("Error", f"Ocurrió un error al generar el informe consolidado:\n{e}")
    finally:
        if wb:
            wb.close()
        if app:
            app.quit()
        gc.collect()  
        
        