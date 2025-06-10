from datetime import time
from datetime import datetime
import os
import xlwings as xw
from tkinter import messagebox
from utils.utils import obtener_fecha_actual
import customtkinter as ctk
import math
from db.egresosDB import *
from models.egresomodelos import *


def capturar_poliza(form,entradas):
        poliza_id = form["poliza_id"].get()
        fecha = form["fecha"].get()
        nombre = form["nombre"].get()
        monto = form["cargo"].get()
        montoletr = form["cargo_letras"].get()
        tipo_pago = form["tipo_pago"].get()
        clave_ref = form["clave_rastreo"].get()
        denominacion = form["denominacion"].get()
        observaciones = form["observaciones"].get()
        
        poliza = PolizaEgreso(
            poliza_id,
            fecha,  
            monto,
            montoletr,
            nombre, 
            tipo_pago,
            clave_ref,
            denominacion,
            observaciones
        )

        for entrada_clave, entrada_desc, entrada_importe in entradas:
            clave = entrada_clave.get().strip()
            #print(f"Advertencia: clave VALOR '{clave}'")
            descripcion = entrada_desc.get()
            partida_especifica = obtener_partida_especifica_por_clave(int(clave))
            cargo = float(entrada_importe.get())
            if clave and descripcion and cargo:
                concepto = ConceptoEgreso(clave, descripcion, partida_especifica, cargo)
                poliza.agregar_concepto(concepto)
                
        return poliza 


def validar_campos_obligatorios_obj(poliza):
    faltantes = poliza.campos_faltantes()
    if faltantes:
        mensaje = "Por favor complete los siguientes campos obligatorios:\n\n" + "\n".join(faltantes)
        messagebox.showerror("Campos incompletos", mensaje)
        return False
    return True

def obtener_valores_campos(form):
    return {
        "fecha": form["fecha"].get(),
        "no_poliza": form["no_poliza"].get(),
        "nombre": form["nombre"].get(),
        "cargo": form["cargo"].get(),
        "cargo_letras": form["cargo_letras"].get(),
        "tipo_pago": form["tipo_pago"].get(),
        "clave_rastreo": form["clave_rastreo"].get(),
        "denominacion": form["denominacion"].get(),
        "observaciones": form["observaciones"].get(),
    }

def asignar_valores_en_hoja(hoja, poliza):
    campos_a_celdas = {
        "fecha": "AQ8",
        "poliza_id": "AX5",
        "nombre": "A9",
        "monto": "AO9",
        "montoletr": "A10",
        "tipo_pago": "T12",
        "clave_ref": "A13",
        "denominacion": "A44",
        "observaciones": "A47",
    }

    for campo, celda in campos_a_celdas.items():
        valor = getattr(poliza, campo, "")
        if campo == "clave_rastreo":
            valor = f"CLAVE DE RASTREO {valor}"
        hoja.range(celda).value = valor

def insertar_entradas_en_hoja(hoja, conceptos, fila_inicial=18):
    for concepto in conceptos:
        if concepto.partida_especifica and concepto.cargo:
            hoja.range(f"B{fila_inicial}").value = concepto.partida_especifica
            hoja.range(f"AV{fila_inicial}").value = float(concepto.cargo)
            fila_inicial += 1
        else:
            messagebox.showerror("Error", "Faltan datos. Verifica que todos los campos estén completos.")
            return False
    return True

def guardar_egresos(poliza):
    try:
        app = xw.App(visible=False)
        wb = app.books.open("assets/plantillas/egresos.xlsx")
        hoja = wb.sheets["01 ene 2025"]
        asignar_valores_en_hoja(hoja, poliza)

        if not insertar_entradas_en_hoja(hoja, poliza.conceptos):
            wb.close()
            return

        fecha_actual = obtener_fecha_actual().replace("/", "-")
        nombre_archivo = f"Poliza_Egresos_{fecha_actual}.xlsx"
        ruta_descargas = os.path.expanduser("~/Documentos/Cecati122/PolizasDeEgresos")
        os.makedirs(ruta_descargas, exist_ok=True)
        ruta_archivo = os.path.join(ruta_descargas, nombre_archivo)

        wb.save(ruta_archivo)
        messagebox.showinfo("Éxito", f"Archivo guardado en: {ruta_archivo}")
        wb.close()
    except Exception as e:
        print("Error al guardar:", e)
        messagebox.showerror("Error", f"No se pudo guardar la información.\n{e}")
                
def guardar_pdf(poliza):
    try:
        if not validar_campos_obligatorios_obj(poliza):
            return
        app = xw.App(visible=False)
        wb = app.books.open("assets/plantillas/egresos.xlsx")
        hoja = wb.sheets["01 ene 2025"]
        
        asignar_valores_en_hoja(hoja, poliza)

        if not insertar_entradas_en_hoja(hoja, poliza.conceptos):
            wb.close()
            return

        fecha_actual = obtener_fecha_actual().replace("/", "-")
        nombre_archivo = f"Poliza_Egresos_{fecha_actual}.pdf"
        ruta_descargas = os.path.expanduser("~/Documentos/Cecati122/PolizasDeEgresos")
        os.makedirs(ruta_descargas, exist_ok=True)
        ruta_pdf = os.path.join(ruta_descargas, nombre_archivo)

        hoja.api.ExportAsFixedFormat(0, ruta_pdf)  # 0 = PDF
        wb.close()
        messagebox.showinfo("Éxito", f"PDF guardado en: {ruta_pdf}")
    except Exception as e:
        print("Error al exportar PDF:", e)
        messagebox.showerror("Error", f"No se pudo exportar como PDF.\n{e}")

class AnimacionDescarga(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Descargando...")
        self.geometry("260x180")
        self.resizable(False, False)
        self.configure(fg_color="#191919")
        self.overrideredirect(True)  # Sin barra de título

        self.canvas = ctk.CTkCanvas(self, width=80, height=80, bg="#191919", highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.35, anchor="center")

        self.texto = ctk.CTkLabel(self, text="Descargando", font=("Arial", 16, "bold"), text_color="#3b82f6", fg_color="transparent")
        self.texto.place(relx=0.5, rely=0.7, anchor="center")
                # Centrar respecto a la ventana principal (master)
        if master is not None:
            self.update_idletasks()
            pantalla_w = self.winfo_screenwidth()
            pantalla_h = self.winfo_screenheight()
            win_w = 260
            win_h = 180
            x = (pantalla_w // 2) - (win_w // 2)
            y = (pantalla_h // 2) - (win_h // 2) - 30  # pequeño ajuste visual
            self.geometry(f"{win_w}x{win_h}+{x}+{y}")

        self.puntos = 0
        self.angulo = 0
        self.animar()

    def animar(self):
        self.canvas.delete("all")
        # Dibuja un círculo giratorio 
        radio = 30
        cx, cy = 40, 40
        for i in range(12):
            ang = math.radians(self.angulo + i * 30)
            x = cx + radio * math.cos(ang)
            y = cy + radio * math.sin(ang)
            color = "#3b82f6" if i == 0 else "#64748b"
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline=color)
        self.angulo = (self.angulo + 30) % 360

        # Texto animado "Descargando..."
        puntos = "." * (self.puntos % 4)
        self.texto.configure(text=f"Descargando{puntos}")
        self.puntos += 1

        self.after(120, self.animar)

def ejecutar_con_loading(funcion, btn_guardar, btn_descargar, contenedor_principal, limpiar_formulario, *args):
    btn_guardar.configure(state="disabled", text="Guardando...")
    btn_descargar.configure(state="disabled", text="Descargando...")

    # Mostrar animación visual
    anim = AnimacionDescarga(contenedor_principal)
    anim.grab_set()  # Hace modal la ventana de animación

    def ejecutar():
        try:
            resultado = funcion(*args)
            if resultado:
                messagebox.showinfo("Éxito", "Poliza Guardada correctamente")
            respuesta = messagebox.askyesno(
                "Nuevo documento",
                "¿Desea crear una nueva póliza?"
            )
            if respuesta:
                limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la información.\n{e}")
        finally:
            anim.destroy()  # Cierra la animación
            btn_guardar.configure(state="normal", text="💾 Guardar")
            btn_descargar.configure(state="normal", text="📥 Descargar")
    contenedor_principal.after(100, ejecutar)
    
def limpiar_formulario(contenedor_principal, mostrar_formulario_egresos, frame_padre):
    respuesta = messagebox.askyesno(
        "Limpiar formulario",
        "¿Está seguro de limpiar el formulario?\nEsta acción no se puede deshacer.",
        icon="warning"
    )
    if respuesta:
        for widget in contenedor_principal.winfo_children():
            widget.destroy()
        mostrar_formulario_egresos(frame_padre)
            
            
def animar_confirmacion(widget):
        """Animación de confirmación mejorada"""
        color_original = widget.cget("fg_color")
        try:
            widget.configure(fg_color="#10b981")
            time.sleep(0.3)
            if widget.winfo_exists():
                widget.configure(fg_color=color_original)
        except:
            pass

def generar_no_poliza(numero, fecha):
    # numero: consecutivo (ejemplo: 1, 2, 3)
    # fecha: objeto datetime o string 'YYYY-MM-DD'
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
    mes = fecha.strftime("%b").lower()  # 'jun'
    anio = fecha.strftime("%y")         # '25'
    return f"{str(numero).zfill(3)}-{mes}-{anio}"

# Ejemplo:
no_poliza = generar_no_poliza(1, "2025-06-10")  # '001-jun-25'