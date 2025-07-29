from ui.home import lanzar_ventana_principal
from utils.rutas import inicializar_base_datos, inicializar_base_datos2

if __name__ == "__main__":
    inicializar_base_datos()
    inicializar_base_datos2()
    lanzar_ventana_principal()
