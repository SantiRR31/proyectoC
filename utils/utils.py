import json
import tkinter as tk
import datetime
import os
from utils.rutas import ruta_absoluta

CONFIG_PATH = ruta_absoluta("config.json")

def cargar_config():
    # Valores por defecto
    defaults = {
        "carpeta_destino": "~/Documentos/Cecati122/Polizas",
        "clave_cecati": "22DBT0005P",
        "banco_caja": "BANORTE",
        "geometry": "1280x720+100+100",
        "state": "normal",
        "appearance_mode": "dark",
        "color_theme": "blue"
    }
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            try:
                config = json.load(f)
            except Exception:
                config = {}
    # Asegura que todas las claves existan
    for key, value in defaults.items():
        if key not in config:
            config[key] = value
    return config


def obtener_fecha_actual():
    """Devuelve la fecha actual en formato 'DD/mmm/YYYY', por ejemplo: 01/ene/2025."""
    meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    ahora = datetime.datetime.now()
    return ahora.strftime(f"%d-{meses[ahora.month-1]}%Y")

def abrir_carpeta(ruta_base, subcarpeta=""):
    import os
    # Expandir ~ al directorio del usuario
    ruta_expandida = os.path.expanduser(ruta_base)
    ruta_final = os.path.join(ruta_expandida, subcarpeta) if subcarpeta else ruta_expandida

    # Crear la carpeta si no existe
    if not os.path.exists(ruta_final):
        os.makedirs(ruta_final, exist_ok=True)

    # Abrir la carpeta
    os.startfile(ruta_final)

def convertir_a_mayusculas(entry_widget, event=None):
    texto = entry_widget.get()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, texto.upper())
    
    
    
def solo_numeros_enteros(texto):
    return texto.isdigit() or texto == ""

def solo_numeros_decimales(texto):
    if texto == "":
        return True
    try:
        float(texto)
        return True
    except ValueError:
        return False

def solo_letras(texto):
    return all(letra.isalpha() or letra.isspace() for letra in texto)

def solo_numeros_y_letras(texto):
    return all(letra.isalnum() or letra.isspace() for letra in texto)
        
def numero_a_letras_mxn(numero):
    """
    Convierte un número a letras en formato de moneda mexicana.
    Ejemplo: 873.21 -> (OCHOCIENTOS SETENTA Y TRES PESOS 21/100 M.N.)
    """
    import math

    UNIDADES = (
        '', 'UN', 'DOS', 'TRES', 'CUATRO', 'CINCO', 'SEIS', 'SIETE', 'OCHO', 'NUEVE', 'DIEZ',
        'ONCE', 'DOCE', 'TRECE', 'CATORCE', 'QUINCE', 'DIECISÉIS', 'DIECISIETE', 'DIECIOCHO', 'DIECINUEVE', 'VEINTE'
    )
    DECENAS = (
        'VEINTI', 'TREINTA', 'CUARENTA', 'CINCUENTA', 'SESENTA', 'SETENTA', 'OCHENTA', 'NOVENTA', 'CIEN'
    )
    CENTENAS = (
        '', 'CIENTO', 'DOSCIENTOS', 'TRESCIENTOS', 'CUATROCIENTOS', 'QUINIENTOS', 'SEISCIENTOS',
        'SETECIENTOS', 'OCHOCIENTOS', 'NOVECIENTOS'
    )

    def convertir_grupo(n):
        output = ''
        centenas = n // 100
        decenas = n % 100
        if n == 0:
            return ''
        if n == 100:
            return 'CIEN'
        if centenas > 0:
            output += CENTENAS[centenas] + ' '
        if decenas <= 20:
            output += UNIDADES[decenas]
        else:
            dec = decenas // 10
            uni = decenas % 10
            if decenas < 30:
                output += DECENAS[0] + UNIDADES[uni]
            else:
                output += DECENAS[dec - 2]
                if uni > 0:
                    output += ' Y ' + UNIDADES[uni]
        return output.strip()

    entero = int(math.floor(numero))
    centavos = int(round((numero - entero) * 100))

    if entero == 0:
        letras = 'CERO'
    else:
        letras = ''
        millones = entero // 1000000
        miles = (entero - millones * 1000000) // 1000
        cientos = entero % 1000

        if millones > 0:
            if millones == 1:
                letras += 'UN MILLÓN '
            else:
                letras += convertir_grupo(millones) + ' MILLONES '
        if miles > 0:
            if miles == 1:
                letras += 'MIL '
            else:
                letras += convertir_grupo(miles) + ' MIL '
        if cientos > 0:
            letras += convertir_grupo(cientos)
        letras = letras.strip()

    return f"({letras} PESOS {centavos:02d}/100 M.N.)"



