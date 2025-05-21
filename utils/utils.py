import tkinter as tk
import datetime
import os

def obtener_fecha_actual():
    """Devuelve la fecha actual en formato 'DD/mmm/YYYY', por ejemplo: 01/ene/2025."""
    meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    ahora = datetime.datetime.now()
    return ahora.strftime(f"%d-{meses[ahora.month-1]}%Y")

def abrir_carpeta():
    carpeta_descargas = os.path.expanduser("~/Documentos/Cecati122/PolizasDeIngresos")
    if not os.path.exists(carpeta_descargas):
        os.makedirs(carpeta_descargas, exist_ok=True)
        os.startfile(carpeta_descargas)
        
    

def abrir_carpeta(ruta):
    import os
    carpeta = os.path.dirname(os.path.abspath(ruta))
    if not os.path.exists(carpeta):
        os.makedirs(carpeta, exist_ok=True)
    os.startfile(carpeta)

        
        
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