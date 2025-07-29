import os
import sys
import shutil
from pathlib import Path
from dotenv import load_dotenv

NOMBRE_APP = "GestorEgresosIngresos"
NOMBRE_BD = "prueba2.db"
NOMBRE_BD2 = "prueba.db"

def ruta_absoluta(ruta_relativa):
    """Devuelve la ruta absoluta, compatible con PyInstaller."""
    if getattr(sys, 'frozen', False):  # Si está empaquetado con PyInstaller
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)

# Cargar variables de entorno (.env)
dotenv_path = ruta_absoluta(".env")
load_dotenv(dotenv_path)

def obtener_ruta_appdata(nombre_archivo=""):
    ruta_base = os.path.join(os.environ["LOCALAPPDATA"], NOMBRE_APP)
    os.makedirs(ruta_base, exist_ok=True)
    return os.path.join(ruta_base, nombre_archivo) if nombre_archivo else ruta_base

def inicializar_base_datos():
    try:
        ruta_destino = obtener_ruta_appdata(NOMBRE_BD)
        if not os.path.exists(ruta_destino):
            ruta_origen = Path(ruta_absoluta(os.path.join("db", NOMBRE_BD)))
            if ruta_origen.exists():
                shutil.copy(ruta_origen, ruta_destino)
                print(f"[✓] Base de datos '{NOMBRE_BD}' copiada a: {ruta_destino}")
            else:
                print(f"[!] No se encontró la base de datos '{NOMBRE_BD}' en 'db'.")
    except Exception as e:
        print(f"[✗] Error al copiar '{NOMBRE_BD}': {e}")

def inicializar_base_datos2():
    try:
        ruta_destino = obtener_ruta_appdata(NOMBRE_BD2)
        if not os.path.exists(ruta_destino):
            ruta_origen = Path(ruta_absoluta(NOMBRE_BD2))
            if ruta_origen.exists():
                shutil.copy(ruta_origen, ruta_destino)
                print(f"[✓] Base de datos '{NOMBRE_BD2}' copiada a: {ruta_destino}")
            else:
                print(f"[!] No se encontró la base de datos '{NOMBRE_BD2}' en el directorio actual.")
    except Exception as e:
        print(f"[✗] Error al copiar '{NOMBRE_BD2}': {e}")
