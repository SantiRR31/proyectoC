import sqlite3
import os
import xlwings as xw
import subprocess
import customtkinter as ctk
from tkinter import messagebox
from utils.rutas import ruta_absoluta
from datetime import datetime

def seleccionar_poliza():
    ventana = ctk.CTkToplevel()
    ventana.title("Seleccionar Poliza")
    ventana.geometry("300x300")
    ventana.resizable(False, False)
    
    ctk.CTkLabel(ventana, text="Selecciona el numero de poliza:").pack(pady=(20,10))
    
    combo_dia = ctk.CTkComboBox(ventana, values=[f"{i:02}" for i in range(1, 32)], state="readonly")
    combo_dia.pack(pady=2)
    
    meses = ["ene.", "feb.", "mar.", "abr.", "may.", "jun.", "jul.", "ago.", "sep.", "oct.", "nov.", "dic."]
    combo_mes = ctk.CTkComboBox(ventana, values=meses, state="readonly")
    combo_mes.pack(pady=2)
    
    combo_anio = ctk.CTkComboBox(ventana, values=[str(y) for y in range(2024, datetime.now().year + 1)], state="readonly")
    combo_anio.pack(pady=2)
    
    ctk.CTkLabel(ventana, text="Selecciona la póliza:").pack(pady=(15, 5))
    combo_poliza = ctk.CTkComboBox(ventana, values=[], state="readonly")
    combo_poliza.pack(pady=5)
    
    def actualizar_resultados(*_):
        
        dia = combo_dia.get()
        mes = combo_mes.get()
        anio = combo_anio.get()
        
        print("Buscando con:", dia, mes, anio)
        
        partes=[]
        
        if dia:
            partes.append(dia)
        if mes:
            partes.append(mes)
        if anio:
            partes.append(anio)
            
        if not partes:
            combo_poliza.configure(values=["Sin resultados"])
            combo_poliza.set("No hay resultados")
            return
            
        filtro = "%" + "/".join(partes) + "%"

        try:
            conn = sqlite3.connect("db/prueba2.db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT no_poliza FROM polizasEgresos WHERE no_poliza LIKE ?", (filtro,))
            resultados = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            print("Resultados encontrados:", resultados)
        
            if resultados:
                combo_poliza.configure(values=resultados)
                combo_poliza.set(resultados[0])
            else:
                combo_poliza.configure(values=["Sin resultados"])
                combo_poliza.set("No hay resultados")
        except Exception as e:
            combo_poliza.configure(values="Error de busqueda")
            combo_poliza.set(f"Error: {str(e)}")
        
    combo_dia.configure(command=lambda _: actualizar_resultados())
    combo_mes.configure(command=lambda _: actualizar_resultados())
    combo_anio.configure(command=lambda _: actualizar_resultados())
    
    def confirmar():
        seleccion = combo_poliza.get()
        if seleccion and "No hay" not in seleccion:
            generar_notitas(seleccion)
            ventana.destroy()
    
    ctk.CTkButton(ventana, text="Confirmar", command=confirmar).pack(pady=10)
        

def generar_notitas(no_poliza):
    app = None
    try:
        # Conectar con la base de datos
        conn = sqlite3.connect('db/prueba2.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT observaciones FROM polizasEgresos WHERE no_poliza = ?", (no_poliza,))
        resultado = cursor.fetchone()
        conn.close()
        
        if not resultado:
            messagebox.showerror("Error", f"No se encontró la póliza {no_poliza}")
            return
        
        nota = resultado[0]
        
        #try: 
        #    fecha_dt = datetime.strptime(fecha_str, "%d/%m/%Y")
        #except ValueError:
        #    fecha_dt = datetime.today()
        
        fecha_dt = datetime.today()
            
        nombre_hoja1 = f"COMPERCO {fecha_dt.strftime('%d %B %Y')}"
        nombre_hoja1 = nombre_hoja1[:31]
        
        nombre_hoja2 = f"OCOMI {fecha_dt.strftime('%d %B %Y')}"
        nombre_hoja2 = nombre_hoja2[:31]
            
        ruta_plantilla1 = ruta_absoluta("assets/plantillas/plantillaCOMPERCO.xls")
        ruta_plantilla2 = ruta_absoluta("assets/plantillas/plantillaOCOMI.xls")
        
        ruta_salida1 = os.path.join("C:\\Cecati122\\Observaciones", f"COMPERCO.xls")
        ruta_salida2 = os.path.join("C:\\Cecati122\\Observaciones", f"OCOMI.xls")
        os.makedirs(os.path.dirname(ruta_salida1), exist_ok=True)
        os.makedirs(os.path.dirname(ruta_salida2), exist_ok=True)
        
        app = xw.App(visible=False)
        
        if os.path.exists(ruta_salida1):
            wb1 = app.books.open(ruta_salida1)
        else:
            wb1 = app.books.open(ruta_plantilla1)
            
        #wb1 = app.books.open(ruta_plantilla1)
        hojaBase1 = wb1.sheets[0]
        hojaNueva1 = hojaBase1.copy(after=wb1.sheets[len(wb1.sheets)-1])
        hojaNueva1.name = nombre_hoja1
        hojaNueva1.range("A23").value = nota
        wb1.save(ruta_salida1)
        wb1.close()
            
        if os.path.exists(ruta_salida2):
            wb2 = app.books.open(ruta_salida2)
        else:
            wb2 = app.books.open(ruta_plantilla2)
        
        #wb2 = app.books.open(ruta_plantilla2)
        hojaBase2 = wb2.sheets[0]
        hojaNueva2 = hojaBase2.copy(after=wb2.sheets[len(wb2.sheets)-1])
        hojaNueva2.name = nombre_hoja2
        hojaNueva2.range("A37").value = nota
        wb2.save(ruta_salida2)
        wb2.close()
        
        #Abrir los archivos despues de generarlos
        subprocess.Popen(['start', ruta_salida1], shell=True)
        subprocess.Popen(['start', ruta_salida2], shell=True)
        
        messagebox.showinfo(
            "Exito!",
            f"Notas insertadas en: {nombre_hoja1} y {nombre_hoja2} \nEn los archivos: COMPERCO.xls y OCOMI.xls"
        )
        
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
    finally:
        if app:
            app.quit()
    