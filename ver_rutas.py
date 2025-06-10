import os
import re

# Carpetas o patrones que quieres analizar
carpetas_objetivo = ['assets', 'db', 'styles', 'utils', 'functions', 'ui']
extensiones_objetivo = ('.xlsx', '.db', '.png', '.jpg', '.json', '.css', '.txt')

# Patrón para detectar posibles rutas relativas en funciones comunes
patrones_busqueda = [
    r'open\(["\'](.+?)["\']',                      # open("archivo")
    r'load_workbook\(["\'](.+?)["\']',             # load_workbook("plantilla.xlsx")
    r'Image\.open\(["\'](.+?)["\']',               # Image.open("imagen.png")
    r'read_csv\(["\'](.+?)["\']',                  # pd.read_csv("archivo.csv")
    r'QPixmap\(["\'](.+?)["\']',                   # QPixmap("assets/logo.png")
]

# Recorrer todos los archivos .py del proyecto
for root, _, files in os.walk("."):
    for archivo in files:
        if archivo.endswith(".py"):
            ruta_archivo = os.path.join(root, archivo)
            with open(ruta_archivo, encoding="utf-8", errors="ignore") as f:
                lineas = f.readlines()

            for i, linea in enumerate(lineas, start=1):
                for patron in patrones_busqueda:
                    match = re.search(patron, linea)
                    if match:
                        ruta_relativa = match.group(1)
                        if ruta_relativa.startswith(tuple(carpetas_objetivo)) and ruta_relativa.endswith(extensiones_objetivo):
                            print(f"📍 Posible ruta en: {ruta_archivo} (línea {i})")
                            print(f"   👉 {linea.strip()}")
                            print(f"   ⚠️  Reemplazar por: ruta_absoluta('{ruta_relativa}')\n")