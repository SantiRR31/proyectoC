import tkinter as tk
import datetime
import os
import sqlite3
import subprocess
import xlwings as xw
import shutil
from datetime import datetime
from tkinter import messagebox

def obtener_fecha_actual():
    """Devuelve la fecha actual en formato 'DD-MM-AAAA'."""
    return datetime.now().strftime("%d-%m-%Y")


def abrir_carpeta():
    carpeta_descargas = r"C:\Cecati122"
    if not os.path.exists(carpeta_descargas):
        os.makedirs(carpeta_descargas)
    
    subprocess.Popen(f'explorer "{carpeta_descargas}"')
    
def buscar_denominacion_db(clave):
        conn = sqlite3.connect('prueba.db')
        cursor = conn.cursor()
        cursor.execute("SELECT denominacion FROM partidasIngresos WHERE partida = ?", (clave,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else "No encontrada"
    
def confirmar_y_generar():
    respuesta = messagebox.askyesno("Generar Informe Consolidado de Ingresos", "¿Está seguro de generar el reporte?")
    if respuesta:
        gen_inf_consolidado()
    
meses_esp = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
# Funcion para generar el informe consolidado de ingresos
def gen_inf_consolidado():
    xw.App(visible=False).display_alerts = False  # Esto evita usar instancias visibles

    hoy = datetime.today()
    anio = str(hoy.year)
    mes_num = hoy.strftime("%m")
    mes_texto = meses_esp[hoy.month - 1]
    # Valores fijos para mayo 2025
    #anio = "2025"
    #mes_num = "05"
    #mes_texto = "mayo"
    
    nom_archivo = f"ingresos_{anio}-{mes_num}.xlsx"
    nom_hoja = f"{mes_texto} {anio}"
    
    carpeta_informes = r"C:\Cecati122\InformesDeIngresos"
    ruta_archivo_origen = os.path.join(carpeta_informes,nom_archivo)
    ruta_archivo_destino = os.path.join("assets", "plantillaConsolidadoIngresos.xls")
    
    carpeta_destino = r"C:\Cecati122\Consolidado Ingresos"
    os.makedirs(carpeta_destino, exist_ok=True)
    ruta_nueva = os.path.join(carpeta_destino, f"consolidado_ingresos_{anio}-{mes_num}.xls")
    
    shutil.copy(ruta_archivo_destino, ruta_nueva)
    
    if not os.path.exists(ruta_archivo_origen):
        print(f"Archivo {nom_archivo} no encontrado")
        messagebox.showerror("Error", f"Archivo {nom_archivo} no encontrado, asegurese de haberlo generado previamente.")  
        
    else:
        wb_origen = xw.Book(ruta_archivo_origen, update_links=False, visible=False)
        hoja_origen = wb_origen.sheets[nom_hoja]
        
        fila_claves = hoja_origen.range("D8").expand("right").value
        #print("Fila de claves:", fila_claves)
        
        fila_totales = hoja_origen.range("D41").expand("right").value
        #print("Fila de totales:", fila_totales)
        
        # ----------------------------------------------
        # BLOQUE PARA CLAVES CON A
        celdas_claves = ["C17", "C19", "C21", "C23"]
        celdas_totales = ["H17", "H19", "H21", "H23"]
        
        wb_destino = xw.Book(ruta_nueva, update_links=False, visible=False)
        hoja_destino = wb_destino.sheets.active
        
        # Contador para ubicar las claves A
        idx_destino = 0
        
        for clave, total in zip(fila_claves, fila_totales):
            if isinstance(clave, str) and clave.startswith("A") and idx_destino < len(celdas_claves):
                hoja_destino.range(celdas_claves[idx_destino]).value = clave
                hoja_destino.range(celdas_totales[idx_destino]).value = total
                idx_destino += 1
        # ----------------------------------------------
        # BLOQUE PARA CLAVES CON B
        celdas_claves_b = ["C33", "C35", "C37", "C39", "C41"]
        celdas_totales_b = ["H33", "H35", "H37", "H39", "H41"]
        
        idx_destino_b = 0
        
        for clave, total in zip(fila_claves, fila_totales):
            if isinstance(clave, str) and clave.startswith("B") and idx_destino_b < len(celdas_claves_b):
                hoja_destino.range(celdas_claves_b[idx_destino_b]).value = clave
                hoja_destino.range( celdas_totales_b[idx_destino_b]).value = total
                idx_destino_b += 1
        # ----------------------------------------------
        # BLOQUE PARA CLAVES CON C
        celdas_claves_c = ["R26", "R29", "R31", "R34"]
        celdas_totales_c = ["W26", "W29", "W31", "W34"]
        
        idx_destino_c = 0
        
        for clave, total in zip(fila_claves, fila_totales):
            if isinstance(clave, str) and clave.startswith("C") and idx_destino_c < len(celdas_claves_c):
                hoja_destino.range(celdas_claves_c[idx_destino_c]).value = clave
                hoja_destino.range(celdas_totales_c[idx_destino_c]).value = total
                idx_destino_c += 1
        # ----------------------------------------------
        # BLOQUE PARA CLAVES CON D
        celdas_claves_d = ["AG19", "AG21", "AG23", "AG25"]
        celdas_totales_d = ["AL19", "AL21", "AL23", "AL25"]
        
        idx_destino_d = 0
        
        for clave, total in zip(fila_claves, fila_totales):
            if isinstance(clave, str) and clave.startswith("D") and idx_destino_d < len(celdas_claves_d):
                hoja_destino.range(celdas_claves_d[idx_destino_d]).value = clave
                hoja_destino.range(celdas_totales_d[idx_destino_d]).value = total
                idx_destino_d += 1
        # BLOQUE PARA LAS CLAVES ESPECIALES DE DEUDORES Y ACREEDORES
        for clave, total in zip(fila_claves, fila_totales):
            if clave == 120:
                hoja_destino.range("AL39").value = total
            elif clave == 330:
                hoja_destino.range("AL40").value = total
                
                
        fecha = datetime.now()
        mes_informado = f"{meses_esp[fecha.month - 1]} {fecha.year}"
        fecha_elab = fecha.strftime("%d %m %Y")
        
        hoja_destino.range("R9").value = mes_informado
        hoja_destino.range("AH9").value = fecha_elab
        
        wb_destino.save()
        wb_destino.close()
        
        wb_origen.close()
                
        messagebox.showinfo("Éxito", "Transferencia de claves y totales completada")