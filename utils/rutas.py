import os
import sys

def ruta_absoluta(ruta_relativa):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)