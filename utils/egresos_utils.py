import os
import xlwings as xw
from tkinter import messagebox
from utils.utils import obtener_fecha_actual
import customtkinter as ctk

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

def asignar_valores_en_hoja(hoja, datos):
    campos_a_celdas = {
        "fecha": "AQ8",
        "no_poliza": "AX5",
        "nombre": "A9",
        "cargo": "AO9",
        "cargo_letras": "A10",
        "tipo_pago": "T12",
        "clave_rastreo": "A13",
        "denominacion": "A44",
        "observaciones": "A47",
    }

    for campo, celda in campos_a_celdas.items():
        valor = datos[campo]
        if campo == "clave_rastreo":
            valor = f"CLAVE DE RASTREO {valor}"
        hoja.range(celda).value = valor

def insertar_entradas_en_hoja(hoja, entradas, fila_inicial=18):
    for i, (entrada_clave, entrada_resultado, entrada_abono) in enumerate(entradas):
        clave = entrada_clave.get()
        denominacion = entrada_resultado.get()
        cargo = entrada_abono.get()

        if clave and denominacion and cargo:
            hoja.range(f"B{fila_inicial}").value = clave
            hoja.range(f"AV{fila_inicial}").value = float(cargo)
            fila_inicial += 1
        else:
            messagebox.showerror("Error", "Faltan datos. Verifica que todos los campos estén completos.")
            return False
    return True

def guardar_egresos(form, entradas):
    try:
        app = xw.App(visible=False)
        wb = app.books.open("assets/plantillas/egresos.xlsx")
        hoja = wb.sheets["01 ene 2025"]

        datos = obtener_valores_campos(form)
        asignar_valores_en_hoja(hoja, datos)

        if not insertar_entradas_en_hoja(hoja, entradas):
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


#import customtkinter as ctk

class AnimacionDescarga(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Descargando...")
        self.geometry("300x300")
        self.resizable(False, False)

        self.paper = ctk.CTkLabel(self, text="||||\n||||\n||||", 
                                  fg_color="#EEF0FD", text_color="#D3D4EC",
                                  corner_radius=5, width=80, height=60,
                                  anchor="n", font=("Courier", 12))
        self.paper.place(x=110, y=200)

        self.keyboard = ctk.CTkFrame(self, width=120, height=60, fg_color="#275EFE", corner_radius=10)
        self.keyboard.place(x=90, y=240)

        self.keys = []
        key_positions = [(10,10), (30,10), (50,10), (70,10), (90,10),
                         (20,30), (40,30), (60,30), (80,30)]

        for x, y in key_positions:
            key = ctk.CTkLabel(self.keyboard, width=10, height=5, text="", fg_color="white", corner_radius=2)
            key.place(x=x, y=y)
            self.keys.append(key)

        self.paper_y = 200
        self.direction = -1
        self.key_index = 0
        self.animate()

    def animate(self):
        self.paper_y += self.direction * 1
        if self.paper_y < 120 or self.paper_y > 200:
            self.direction *= -1
        self.paper.place_configure(y=self.paper_y)

        for i, key in enumerate(self.keys):
            key.configure(fg_color="white" if i == self.key_index else "#275EFE")
        self.key_index = (self.key_index + 1) % len(self.keys)

        self.after(100, self.animate)




def descargar_con_animacion(form, entradas):
    animacion = AnimacionDescarga()
    animacion.after(10000, animacion.destroy)  # Cierra después de 3 segundos
    guardar_egresos(form, entradas)  # Ejecuta tu lógica real
