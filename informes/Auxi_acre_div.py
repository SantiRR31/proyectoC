from datetime import datetime
from tkinter import ttk, messagebox
import customtkinter as ctk
from db.auxDB import obtener_partidas_i_330_mes, obtener_partidas_e_330_mes
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

def confirmar_y_generar_Auxiliar_acree(contenedor_principal=None):
    ventana = ctk.CTkToplevel()
    ventana.title("Generar informe auxiliar de acreedores")
    ventana.geometry("340x220")
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
    saldo_var = ctk.StringVar(value="")

    mes_cb = ttk.Combobox(frame, values=meses_lista, textvariable=mes_var, state="readonly", width=14)
    mes_cb.grid(row=0, column=0, padx=8)
    anio_cb = ttk.Combobox(frame, values=[str(a) for a in range(anio_actual-5, anio_actual+2)], textvariable=anio_var, width=8, state="readonly")
    anio_cb.grid(row=0, column=1, padx=8)

    saldo_frame = ctk.CTkFrame(ventana, fg_color="transparent")
    saldo_frame.pack(pady=4)
    ctk.CTkLabel(saldo_frame, text="Saldo inicial:", font=("Arial", 12)).grid(row=0, column=0, padx=8)
    saldo_entry = ctk.CTkEntry(saldo_frame, textvariable=saldo_var, width=120)
    saldo_entry.grid(row=0, column=1, padx=8)

    def generar_reporte_seleccionado():
        saldo_inicial = saldo_var.get().strip()
        if not saldo_inicial:
            messagebox.showerror("Error", "Debe ingresar el saldo inicial.")
            return
        try:
            saldo_inicial_float = float(saldo_inicial)
        except ValueError:
            messagebox.showerror("Error", "El saldo inicial debe ser un número.")
            return
        mes_idx = meses_lista.index(mes_var.get()) + 1
        anio = int(anio_var.get())
        mes_str = f"{anio}-{mes_idx:02d}"
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            lambda: gen_Aux_acre_div(saldo_inicial_float, mes_str),
            contenedor_principal=contenedor_principal,
        )

    def generar_reporte_actual():
        saldo_inicial = saldo_var.get().strip()
        if not saldo_inicial:
            messagebox.showerror("Error", "Debe ingresar el saldo inicial.")
            return
        try:
            saldo_inicial_float = float(saldo_inicial)
        except ValueError:
            messagebox.showerror("Error", "El saldo inicial debe ser un número.")
            return
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            lambda: gen_Aux_acre_div(saldo_inicial_float),
            contenedor_principal=contenedor_principal,
        )

    btn_frame = ctk.CTkFrame(ventana, fg_color="transparent")
    btn_frame.pack(pady=18)

    ctk.CTkButton(btn_frame, text="Generar mes seleccionado", command=generar_reporte_seleccionado, width=140).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Generar mes actual", command=generar_reporte_actual, width=120).pack(side="left", padx = 10)
    
    
def gen_Aux_acre_div(saldo_inicial, mes_anio=None):
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
        
        #partidas
        partidas_330_egresos = obtener_partidas_e_330_mes(mes_actual)
        partidas_330_ingresos = obtener_partidas_i_330_mes(mes_actual)
        print(f"Partidas 330 Egresos: {partidas_330_egresos}")
        print(f"Partidas 330 Ingresos: {partidas_330_ingresos}")
        fila_inicio = 15
        
        if not partidas_330_egresos and not partidas_330_ingresos:
            messagebox.showwarning("No hay datos", "No se encontraron partidas 120 para el mes seleccionado.")
            return
        
        app = xw.App(visible=False)
        wb= app.books.open("assets/plantillas/Auxiliar de acredores diversos.xls")
        sht = wb.sheets[0]
        
        #Datos generales
        sht.range("B7").value = f"{config['banco_caja']} S.A." #Nombre del banco
        sht.range("T7").value = config['no_cuenta'] #Numero de cuenta
        sht.range("AG4").value = config['no_cecati'] # Numero de la institucion
        sht.range("AH7").value = dia
        sht.range("AL7").value = mes_excel
        sht.range("AQ7").value = anio_excel
        mes_abrev = mes_nombre[:3]  # 'marzo' -> 'mar'
        anio_corto = anio[-2:]      # '2025' -> '25'
        sht.range("V3").value = f"{mes_abrev}-{anio_corto}"
        sht.range("AO4").value = config['clave_cecati']
        sht.range("AP9").value = saldo_inicial
        
        def fecha_a_yyyymmdd(fecha):
            if "/" in fecha:
                d, m, y = fecha.split("/")
                return f"{y}{m.zfill(2)}{d.zfill(2)}"
            elif "-" in fecha:
                y, m, d = fecha.split("-")
                return f"{y}{m.zfill(2)}{d.zfill(2)}"
            return fecha

        partidas_combinadas = [
            ("Egreso", cargo, fecha) for cargo, fecha in partidas_330_egresos
        ] + [
            ("Ingreso", cargo, fecha) for cargo, fecha in partidas_330_ingresos
        ]

        partidas_ordenadas = sorted(partidas_combinadas, key=lambda x: fecha_a_yyyymmdd(x[2]))
        
        for idx, (tipo, cargo, fecha) in enumerate(partidas_ordenadas):
            fila = fila_inicio + idx
            try:
                # Si fecha es 'DD/MM/YYYY'
                if "/" in fecha:
                    dia, mes, anio = fecha.split("/")
                # Si fecha es 'YYYY-MM-DD'
                elif "-" in fecha:
                    anio, mes, dia = fecha.split("-")
                else:
                    mes, dia = "", ""
                fecha_formateada = f"{mes}-{dia}"
            except Exception:
                fecha_formateada = fecha
            sht.range(f"B{fila}").value = fecha_formateada
            if tipo == "Egreso":
                sht.range(f"AC{fila}").value = cargo
            else:  # Ingreso
                sht.range(f"AJ{fila}").value = cargo
        
        carpeta_salida = os.path.join(config["carpeta_destino"], "Auxiliar Acreedores diversos")
        os.makedirs(carpeta_salida, exist_ok=True)        
        archivo_salida = os.path.join(carpeta_salida, f"{mes_nombre} {anio}.xlsx")
        wb.save(archivo_salida)
        messagebox.showinfo("Reporte generado", f"El Auxiliar de acreedores diversos se ha generado:\n{archivo_salida}")
        return archivo_salida
        
    except Exception as e:
        print(f"Error al generar el auxiliar de acreedores: {e}")
        messagebox.showerror("Error", f"Error al generar el auxiliar de acreedores: {e}")
    finally: 
        if wb:
            wb.close()
        if app:
            app.quit()
        gc.collect()