import tkinter as tk
import datetime
import os
import sqlite3
import subprocess
import xlwings as xw
import shutil
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
import threading
from tkinter import ttk
from utils.rutas import ruta_absoluta


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
    
    
    
def confirmar_y_generar2():
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
    ruta_archivo_destino = ruta_absoluta(os.path.join("assets", "plantillaConsolidadoIngresos.xls"))
    
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
        
def confirmar_aux():
    import tkinter as tk
    parent = tk._default_root
    icon_path = ruta_absoluta("assets/cecati-122.ico")
    ventana_parametros = ctk.CTkToplevel(parent)
    ventana_parametros.title("Seleccionar parámetros")
    ventana_parametros.geometry("350x250")
    ventana_parametros.grab_set()
    ventana_parametros.iconbitmap(icon_path)
    
    # Centramos la ventana
    ventana_parametros.update_idletasks()
    ancho_ventana = 350
    alto_ventana = 250
    ancho_pantalla = ventana_parametros.winfo_screenwidth()
    alto_pantalla = ventana_parametros.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana_parametros.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    ventana_parametros.grab_set()
    
    ctk.CTkLabel(ventana_parametros, text="Selecciona el año y el mes:",
                 font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
    
    # Año
    anios = [str(a) for a in range(2024, datetime.now().year + 2)]
    combo_anio = ctk.CTkComboBox(ventana_parametros, values=anios)
    combo_anio.set(str(datetime.now().year))
    combo_anio.pack(pady=10)

    # Mes
    meses = [str(i) for i in range(1, 13)]
    combo_mes = ctk.CTkComboBox(ventana_parametros, values=meses)
    combo_mes.set(str(datetime.now().month))
    combo_mes.pack(pady=10)
    
    progress = ttk.Progressbar(ventana_parametros, mode='indeterminate', length=250)
    
    def confirmar():
        def generar_archivo():
            try:
                anio = int(combo_anio.get())
                mes = int(combo_mes.get())

                # Mostrar progressbar en el hilo principal
                ventana_parametros.after(0, lambda: progress.pack(pady=10))
                ventana_parametros.after(0, progress.start)

                nombre_archivo, carpeta_destino = gen_aux_bancario(ruta_db, anio, mes)

                # Ocultar progressbar y mostrar mensaje en hilo principal
                def finalizar():
                    progress.stop()
                    progress.pack_forget()
                    success_msg = (
                        "Archivo generado exitosamente!\n"
                        f"Archivo: {nombre_archivo}\n"
                        f"Ubicación: {carpeta_destino}\n"
                    )
                    messagebox.showinfo("Éxito", success_msg)
                    ventana_parametros.destroy()

                ventana_parametros.after(0, finalizar)
            except Exception as e:
                def mostrar_error(err=e):
                    progress.stop()
                    progress.pack_forget()
                    messagebox.showerror("Error", f"Ocurrió un error: {err}")
                ventana_parametros.after(0, mostrar_error)

        threading.Thread(target=generar_archivo).start()
            
    ctk.CTkButton(ventana_parametros, text="Confirmar", command=confirmar).pack(pady=10)
    ctk.CTkButton(ventana_parametros, text="Cancelar", fg_color="gray",
                  command=ventana_parametros.destroy).pack()
    
    
    ruta_db = "prueba.db"
    
    
# Funcion para generar el documento "auxiliar bancario"    
def gen_aux_bancario(ruta_db, anio, mes):
    ruta_plantilla = ruta_absoluta("assets/plantillaAuxBancario.xls")
    carpeta_destino = r"C:\Cecati122\Auxiliar Bancario"
    
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
    
    app = xw.App(visible=False)
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
    app.quit()
    
    return nombre_archivo, carpeta_destino

    
    