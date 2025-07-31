import locale
import tkinter as tk
from datetime import datetime

def obtener_fecha_actual():
    """Devuelve la fecha actual en formato 'DD/mmm/YYYY', por ejemplo: 01/ene/2025."""
    meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    ahora = datetime.now()
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
    permitidos = " -'áéíóúÁÉÍÓÚüÜñÑ."
    return all(letra.isalpha() or letra in permitidos for letra in texto)

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

# Asegúrate de usar el locale español para los nombres de meses
try:
    locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except:
        pass  # Si no está disponible, usará el default

def obtener_nombre_hoja(no_poliza):
    try:
        partes = no_poliza.strip().lower().split("/")
        if len(partes) != 3:
            raise ValueError("Formato inválido")
        dia, mes, anio = partes
        return f"{int(dia):02d} {mes} {anio}"
    except Exception as e:
        print(f"Error procesando poliza_id '{no_poliza}': {e}")
        return "no_poliza inválida"

def obtener_nombre_hoja_desde_mes(mes_anio: str) -> str:
    meses_nombre = {
        "01": "ene", "02": "feb", "03": "mar", "04": "abr", "05": "may", "06": "jun",
        "07": "jul", "08": "ago", "09": "sep", "10": "oct", "11": "nov", "12": "dic"
    }
    anio, mes = mes_anio.split("-")
    return f"{meses_nombre[mes]} {anio}"


def col2int(col):
    """Convierte una referencia de columna de Excel (ej: 'A', 'AG') a número entero (1-indexed)."""
    col = col.upper()
    num = 0
    for c in col:
        num = num * 26 + (ord(c) - ord('A') + 1)
    return num

def agrupar_partidas_por_grupo(partidas_mes):
    grupos = {}
    for codigo, total_cargo in partidas_mes:
        codigo_str = str(codigo)
        if len(codigo_str) == 5:
            grupo = int(codigo_str[:2]) * 100
        elif len(codigo_str) == 4:
            grupo = int(codigo_str[:2]) * 100
        elif len(codigo_str) == 3:
            grupo = int(codigo_str[0]) * 100
        else:
            grupo = int(codigo)
        if grupo not in grupos:
            grupos[grupo] = []
        grupos[grupo].append((codigo, total_cargo))
    return grupos