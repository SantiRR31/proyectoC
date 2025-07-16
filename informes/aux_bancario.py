from datetime import datetime
from tkinter import ttk, messagebox
import customtkinter as ctk
#from db.egresosDb import obtener_partidas_mesagrupasa, agrupar_partidas_por_grupo, obtener_total_acreedores, obtener_total_deudores
from utils.egresos_utils import mostrar_loading_y_ejecutar
from utils.egresos_utils import cargar_config
import gc 
import xlwings as xw
import re
import os  

config = cargar_config()

meses = {
    1:"enero", 2:"febrero", 3:"marzo", 4:"abril",
    5:"mayo", 6:"junio", 7:"julio", 8:"agosto",
    9:"septiembre", 10:"octubre", 11:"noviembre", 12:"diciembre"
    }

def confirmar_y_generar_aux_bancario(contenedor_principal=None):
    ventana = ctk.CTkToplevel()
    ventana.title("Generar Auxiliar bancario")
    ventana.geometry("340x180")
    ventana.resizable(False, False)
    ventana.grab_set()
    
    meses_lista = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    
    hoy = datetime.now()
    mes_actual = hoy.month
    anio_actual = hoy.year
    
    
    
    ctk.CTkLabel(ventana, text = "Seleccione el mes y año del  reporte:", font=("Arial", 13)).pack(pady= (16,6))
    frame = ctk.CTkFrame(ventana, fg_color="transparent")
    frame.pack(pady = 4)    
    
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
            lambda: gen_Aux_acre_div(mes_str),
            contenedor_principal=contenedor_principal,
        )

    def generar_reporte_actual():
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            gen_Aux_acre_div,
            contenedor_principal=contenedor_principal,
        )

    btn_frame = ctk.CTkFrame(ventana, fg_color="transparent")
    btn_frame.pack(pady=18)

    ctk.CTkButton(btn_frame, text="Generar mes seleccionado", command=generar_reporte_seleccionado, width=140).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Generar mes actual", command=generar_reporte_actual, width=120).pack(side="left", padx=10)


def gen_Aux_acre_div(mes_anio= None):
    app = None
    wb = None
    try: 
        hoy = datetime.now()
        mes_actual = mes_anio if mes_anio else hoy.strftime("%Y-%m")
        anio, mes = mes_actual.split('-')
        mes_nombre = meses[int(mes)]
        
        dia = hoy.strftime("%d")
        mes_excel = hoy.strftime("%m")
        anio_excel = hoy.strftime("%Y")
        
        #partidas_mes
        
        app = xw.App(visible=False)
        wb= app.books.open("assets/plantillas/Auxiliar Bancario.xls")
        sht = wb.sheets[0]
        
        #Datos generales
        sht.range("B8").value = config['banco_caja'] #Nombre del banco
        sht.range("Q8").value = config['no_cuenta'] #Numero de cuenta
        sht.range("AI5").value = f"CECATI {config['no_cecati']}" # Numero de la institucion
        sht.range("AQ5").value = f"{config['clave_cecati']}"
        sht.range("AJ8").value = dia
        sht.range("AN8").value = mes_excel
        sht.range("AS8").value = anio_excel
        mes_abrev = mes_nombre[:3]  # 'marzo' -> 'mar'
        anio_corto = anio[-2:]      # '2025' -> '25'
        sht.range("V4").value = f"{mes_abrev}-{anio_corto}"
        
        
        carpeta_salida = os.path.join(config["carpeta_destino"], "Auxiliares", "Bancario")
        os.makedirs(carpeta_salida, exist_ok=True)
        
        
        
        archivo_salida = os.path.join(carpeta_salida, f"Auxiliar_Bancario{mes_abrev}_{anio_corto}.xlsx")
        wb.save(archivo_salida)
        messagebox.showinfo("Reporte generado", f"El Auxiliar bancario se ha generado:\n{archivo_salida}")
        return archivo_salida
        
    except Exception as e:
        print(f"Error al generar el auxiliar bancario: {e}")
        messagebox.showerror("Error", f"Error al generar el auxiliar bancario: {e}")
    finally: 
        if wb:
            wb.close()
        if app:
            app.quit()
        gc.collect()