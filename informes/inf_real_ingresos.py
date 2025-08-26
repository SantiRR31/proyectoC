import sqlite3
import os
import gc
import customtkinter as ctk
from datetime import datetime
from db.conexion import conectar_db2
import xlwings as xw
from tkinter import messagebox
from utils.config_utils import cargar_config
from utils.rutas import ruta_absoluta

config = cargar_config()

meses = [
    "", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
    "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

def confirmar_y_generar_inf_real_ingresos(contenedor_principal=None):
    ventana = ctk.CTkToplevel()
    ventana.title("Informe Real de Ingresos")
    ventana.geometry("340x180")
    ventana.resizable(False, False)
    ventana.grab_set()
    
    
    ctk.CTkLabel(ventana, text="Seleccione el mes y año del reporte:", font=("Arial", 13)).pack(pady=(16, 6))
    
    meses = [f"{i:02}" for i in range(1,13)]
    anios = [str(anio) for anio in range(2023, datetime.now().year + 1)]
    
    frame_cbbox = ctk.CTkFrame(ventana, fg_color = "transparent")
    frame_cbbox.pack(pady=6)
    
    cb_mes = ctk.CTkComboBox(frame_cbbox, values=meses, width=100)
    cb_mes.set(datetime.now().strftime("%m"))
    cb_mes.pack(side="left", padx=10)
    
    cb_anio = ctk.CTkComboBox(frame_cbbox, values=anios, width=100)
    cb_anio.set(datetime.now().strftime("%Y"))
    cb_anio.pack(side="left", padx=10)
    
    def ejecutar_generacion():
        mes = cb_mes.get()
        anio = cb_anio.get()
        mes_anio = f"{anio}-{mes}"
        generar_informe_ingresos(mes_anio)
        ventana.destroy()
        
    ctk.CTkButton(ventana, text="Generar", command=ejecutar_generacion).pack(pady=10)
    
    
def generar_informe_ingresos(mes_anio=None):
    app = None
    wb = None
    try:
        hoy = datetime.now()
        mes_actual = mes_anio if mes_anio else hoy.strftime("%Y-%m")
        anio, mes = mes_actual.split('-')
        mes_nombre = meses[int(mes)]

        partidas_mes = obtener_totales_ingresos(mes_actual)
        if not partidas_mes:
            messagebox.showwarning("Sin datos", "No hay datos de ingresos para el mes y año seleccionados.")
            return
        partidas_por_grupo = agrupar_por_letra_clave(partidas_mes)
        total120 = next((total for clave, total in partidas_mes if clave == "120"), None)
        total330 = next((total for clave, total in partidas_mes if clave == "330"), None)
        
        app = xw.App(visible=False)
        ruta_plantilla = ruta_absoluta("assets/plantillas/PlantillaInformeRealIngresos.xls")
        wb = app.books.open(ruta_plantilla)
        sht = wb.sheets[0]
        
        #print("pasamos la planttilla")

        sht.range("T5").value = config["clave_cecati"]
        sht.range("AL5").value = hoy.strftime("%d %m %Y")
        sht.range("AT5").value = f"{mes_nombre} {anio}"
        sht.range("AC5").value = config["cuenta_cheques"]
        
        #print("pasamos los datos de arriba")

        fila = 12
        for grupo in sorted(partidas_por_grupo):
            sht.range(f"B{fila}").value = grupo
            fila += 1
            for clave, total in partidas_por_grupo[grupo]:
                sht.range(f"B{fila}").value = clave
                sht.range(f"AL{fila}").value = total
                fila += 1
                
        if total120 is not None:
            sht.range("AL41").value = total120
        if total330 is not None:
            sht.range("AL42").value = total330
        
        #print("pasamos los datos de abajo")

        ruta_destino = os.path.join(config["carpeta_destino"], "Informe Real Ingresos")

        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)

        salida = os.path.join(config["carpeta_destino"], f"Informe Real de Ingresos_{mes_nombre} {anio}.xlsx")
        wb.save(salida)
        messagebox.showinfo("Reporte generado", f"El informe real de ingresos se ha generado:\n{salida}")
        return salida

    except Exception as e:
        print(f"Error generando el informe real de ingresos: {e}")
        messagebox.showerror("Error", f"Ocurrió un error al generar el informe real de ingresos:\n{e}")

    finally:
        if wb:
            wb.close()
        if app:
            app.quit()
        gc.collect()

def obtener_totales_ingresos(mes_anio):
    conn = conectar_db2() 
    cursor = conn.cursor()
    cursor.execute("""
        SELECT clave, SUM(abono)
        FROM detallePolizaIngreso
        WHERE substr(fecha, 4, 2) = ? AND substr(fecha, 7, 4) = ?
        GROUP BY clave
        ORDER BY clave;
    """, (mes_anio.split('-')[1], mes_anio.split('-')[0]))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def agrupar_por_letra_clave(partidas_mes):
    grupos = {}
    for clave, total in partidas_mes:
        if clave in ("120", "330"):
            continue
        grupo = f"{clave[0].upper()}000"
        if grupo not in grupos:
            grupos[grupo] = []
        grupos[grupo].append((clave, total))
    return grupos

