import os
import sys
import dotenv
from dotenv import load_dotenv

def ruta_absoluta(ruta_relativa):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)

dotenv_path = ruta_absoluta('.env')
load_dotenv(dotenv_path)