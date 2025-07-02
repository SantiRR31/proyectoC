import locale
import tkinter as tk
from datetime import datetime

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

def obtener_nombre_hoja(poliza_id):
    # poliza_id: "08/jun/2025"
    fecha_dt = datetime.strptime(poliza_id, "%d/%b/%Y")
    # %B para mes completo, %b para abreviado
    return fecha_dt.strftime("%d %B %Y").lower()  # Ejemplo: "08 abril 2025"


def col2int(col):
    """Convierte una referencia de columna de Excel (ej: 'A', 'AG') a número entero (1-indexed)."""
    col = col.upper()
    num = 0
    for c in col:
        num = num * 26 + (ord(c) - ord('A') + 1)
    return num
