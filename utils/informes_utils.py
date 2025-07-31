import gc


def cerrar_recursos(wb, app):
    try:
        if wb:
            wb.close()
    except Exception as e:
        print("Error cerrando el libro:", e)
    try:
        if app:
            app.quit()
    except Exception as e:
        print("Error cerrando Excel:", e)
    gc.collect()
    
    
def eliminar_hoja_si_existe(wb, nombre_hoja):
    try:
        hoja = wb.sheets[nombre_hoja]
        hoja.delete()
    except Exception:
        pass  # Si no existe, no hacemos nada