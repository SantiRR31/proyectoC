import tkinter as tk
import datetime
import os

def obtener_fecha_actual():
    """Devuelve la fecha actual en formato 'DD-MM-AAAA'."""
    return datetime.datetime.now().strftime("%d-%m-%Y")

def abrir_carpeta():
    carpeta_descargas = os.path.expanduser("~/Documentos/Cecati122/PolizasDeIngresos")
    if not os.path.exists(carpeta_descargas):
        os.makedirs(carpeta_descargas, exist_ok=True)
        os.startfile(carpeta_descargas)
