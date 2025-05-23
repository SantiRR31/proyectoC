import tkinter as tk
import datetime
import os
import sqlite3
import subprocess

def obtener_fecha_actual():
    """Devuelve la fecha actual en formato 'DD-MM-AAAA'."""
    return datetime.datetime.now().strftime("%d-%m-%Y")


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

