import os
import json
from utils.rutas import ruta_absoluta
import sys
#CONFIG_PATH = ruta_absoluta("config.json")

DEFAULT_CONFIG = {
    "carpeta_destino": "~/Documentos/Cecati122/Polizas",
    "clave_cecati": "22DBT0005P",
    "cuenta_cheques":"1056897860",
    "banco_caja": "BANORTE",
    "geometry": "1280x720+100+100",
    "state": "normal",
    "appearance_mode": "dark",
    "color_theme": "blue",
    "no_cecati": "000",
    "no_cuenta" : "1234567890",
    "cuenta_cheques": "1056897860"
}

def obtener_ruta_config():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, "config.json")

CONFIG_PATH = obtener_ruta_config()

def cargar_config():
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            try:
                config = json.load(f)
            except Exception:
                config = {}
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
    return config

def guardar_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def actualizar_config(clave, valor):
    config = cargar_config()
    config[clave] = valor
    guardar_config(config)