import tkinter as tk
import datetime


def obtener_fecha_actual():
    """Devuelve la fecha actual en formato 'DD-MM-AAAA'."""
    return datetime.datetime.now().strftime("%d-%m-%Y")