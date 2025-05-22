import os
import xlwings as xw
from tkinter import messagebox
from utils.utils import obtener_fecha_actual

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
            messagebox.showerror("Error", f"Faltan datos en la fila {i + 1}. Verifica que todos los campos estén completos.")
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
        messagebox.showerror("Error", "No se pudo guardar la información. ", e)
