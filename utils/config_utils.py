import os
import json

CONFIG_PATH = "config.json"

def cargar_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            try:
                return json.load(f)
            except Exception:
                pass
    # Valores por defecto
    return {
        "carpeta_destino": "~/Documentos/Cecati122/Polizas",
        "clave_cecati": "22DBT0005P",
        "banco_caja": "BANORTE"
    }

def guardar_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def actualizar_config(clave, valor):
    config = cargar_config()
    config[clave] = valor
    guardar_config(config)