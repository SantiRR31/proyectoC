from datetime import datetime
import customtkinter as ctk
from db.egresosDB import agrupar_partidas_por_grupo, obtener_partidas_mesagrupasa
from utils.config_utils import cargar_config
from utils.egresos_utils import mostrar_loading_y_ejecutar
from utils.rutas import ruta_absoluta
from tkinter import messagebox, ttk
import gc
import os
import xlwings as xw

config = cargar_config()

meses = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def confirmar_y_generar_infReal(contenedor_principal=None):
    ventana = ctk.CTkToplevel()
    ventana.title("Generar informe real de egresos")
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
            lambda: generar_inf_real_egresos(mes_str),
            contenedor_principal=contenedor_principal,
        )

    def generar_reporte_actual():
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            generar_inf_real_egresos,
            contenedor_principal=contenedor_principal,
        )

    btn_frame = ctk.CTkFrame(ventana, fg_color="transparent")
    btn_frame.pack(pady=18)

    ctk.CTkButton(btn_frame, text="Generar mes seleccionado", command=generar_reporte_seleccionado, width=140).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Generar mes actual", command=generar_reporte_actual, width=120).pack(side="left", padx=10)

        
def generar_inf_real_egresos(mes_anio=None):
    app = None
    wb = None
    try:
        hoy = datetime.now()
        mes_actual = mes_anio if mes_anio else hoy.strftime()
        anio, mes = mes_actual.split('-')
        mes_nombre = meses[int(mes)]
        partidas_mes = obtener_partidas_mesagrupasa(mes_actual)
        
        app = xw.App(visible=False)
        wb = app.books.open(ruta_absoluta("assets/plantillas/InformeReal.xls"))
        sht = wb.sheets[0]
        
        # llenar datos generales
        sht.range("AI5").value = config["clave_cecati"] #clave del cecati
        sht.range("AQ5").value = hoy.strftime("%d %m %Y") # Fecha de elaboracion 
        sht.range("AX5").value = f"{mes_nombre} {anio}" # Periodo de infrome 
        sht.range("BB1").value = config["no_cecati"] #no cecati 
        
        # agrupar partidas por grupo: 
        partidas_por_grupo = agrupar_partidas_por_grupo(partidas_mes)
        
        print ("partidasporgrupo",partidas_por_grupo)
        
        fila = 12
        for grupo in sorted(partidas_por_grupo.keys()):
            if grupo in (100,300):
                continue
            partidas = partidas_por_grupo[grupo]
            sht.range(f"B{fila}").value = grupo  # Escribe el grupo solo una vez
            fila += 1
            for codigo, total in partidas:
                if codigo in (120, 330):
                    continue
                sht.range(f"B{fila}").value = codigo  # Ahora sí, la partida específica
                sht.range(f"AQ{fila}").value = total
                fila += 1
        total_120 = None
        total_330 = None
        if 100 in partidas_por_grupo:
            for codigo, total in partidas_por_grupo[100]:
                if codigo == 120:
                    total_120 = total
        if 330 in partidas_por_grupo:
            for codigo, total in partidas_por_grupo[330]:
                if codigo == 330:
                    total_330 = total
        # Si 120 viene como partida suelta (no agrupada en 100)
        if total_120 is None:
            for grupo, partidas in partidas_por_grupo.items():
                for codigo, total in partidas:
                    if codigo == 120:
                        total_120 = total
        if total_330 is None:
            for grupo, partidas in partidas_por_grupo.items():
                for codigo, total in partidas:
                    if codigo == 330:
                        total_330 = total

        if total_120 is not None:
            sht.range("AQ49").value = total_120
        if total_330 is not None:
            sht.range("AQ50").value = total_330
        
        archivo_salida = os.path.join(config["carpeta_destino"], f"InformeReal_{mes_actual}.xlsx")
        wb.save(archivo_salida)
        messagebox.showinfo("Reporte generado", f"El informe real se ha generado:\n{archivo_salida}")
        return archivo_salida
    except Exception as e:
        print(f"Error generando el informe real de egresos:{e}")
        messagebox.showerror("Error", f"Ocurrió un error al generar el informe real:\n{e}")
        
    finally:
        if wb:
            wb.close()
        if app:
            app.quit()
        gc.collect()
        
        
    