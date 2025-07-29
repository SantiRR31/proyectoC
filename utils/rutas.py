import os
import sys
import dotenv
from dotenv import load_dotenv
import shutil
from pathlib import Path

def ruta_absoluta(ruta_relativa):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)

dotenv_path = ruta_absoluta('.env')
load_dotenv(dotenv_path)


NOMBRE_APP = "GestorEgresosIngresos"
NOMBRE_BD = "prueba2.db"


def obtener_ruta_appdata(nombre_archivo=""):
    ruta_base = os.path.join(os.environ["LOCALAPPDATA"], NOMBRE_APP)
    os.makedirs(ruta_base, exist_ok=True)
    return os.path.join(ruta_base, nombre_archivo) if nombre_archivo else ruta_base

def inicializar_base_datos():
    ruta_destino = obtener_ruta_appdata(NOMBRE_BD)
    if not os.path.exists(ruta_destino):
        ruta_origen = Path("db") / NOMBRE_BD
        if ruta_origen.exists():
            shutil.copy(ruta_origen, ruta_destino)
            print(f"Base de datos copiada a: {ruta_destino}")
        else:
            print("No se encontró la base de datos original para copiar.")


