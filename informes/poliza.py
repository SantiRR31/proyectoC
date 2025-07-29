
import traceback
from utils.config_utils import cargar_config
from utils.egresos_utils import validar_campos_obligatorios_obj
import xlwings as xw
from datetime import datetime
from tkinter import messagebox
import os
from utils.rutas import ruta_absoluta
from utils.utils import obtener_fecha_actual, obtener_nombre_hoja
config = cargar_config()

def asignar_valores_en_hoja(hoja, poliza):
    campos_a_celdas = {
        "fecha": "AQ8",
        "no_poliza": "AX5",
        "nombre": "A9",
        "monto": "AO9",
        "monto_letra": "A10",
        "tipo_pago": "T12",
        "clave_ref": "A13",
        "denominacion": "A44",
        "observaciones": "A47",
    }

    for campo, celda in campos_a_celdas.items():
        valor = getattr(poliza, campo, "")
        if campo == "no_poliza":
            try:
                d, m, y = valor.split("/")
                m = m.replace(".", "")  # Eliminar el punto de la abreviatura del mes
                valor = f"{d}/{m}/{y}"
            except Exception:
                pass
            valor = f"{valor}"  # El apóstrofe fuerza a texto en Excel
        if campo == "clave_ref":
            if poliza.tipo_pago == "CHEQUE":
                valor = f"NO. DE CHEQUE {poliza.no_cheque or ''}"
            elif poliza.tipo_pago == "TRANSF. ELECTRÓNICA":                
                valor = f"CLAVE DE RASTREO {poliza.clave_ref or ''}"
            else:
                valor = ""
        if campo == "fecha":
            try:
                d, m, y = valor.split("/")
                valor = f"{m}/{d}/{y}"
            except Exception:
                pass
            valor = f"{valor}" # El apóstrofe fuerza a texto en Excel
        hoja.range(celda).value = valor
        

def insertar_entradas_en_hoja(hoja, conceptos, fila_inicial=18):
    try:
        partidas_sumadas = {}
        for concepto in conceptos:
            if concepto.partida_especifica and concepto.cargo:
                clave = concepto.partida_especifica
                if clave not in partidas_sumadas:
                    partidas_sumadas[clave] = {"total": 0}
                partidas_sumadas[clave]["total"] += float(concepto.cargo)
            else:
                messagebox.showerror("Error", "Faltan datos. Verifica que todos los campos estén completos.")
                return False
        for partida, datos in partidas_sumadas.items():
            hoja.range(f"B{fila_inicial}").value = partida
            hoja.range(f"AV{fila_inicial}").value = datos["total"]
            fila_inicial += 1
        return True
    except Exception as e:
        print("Error al insertar entradas en la hoja:", e)
        messagebox.showerror("Error", f"No se pudieron insertar los conceptos.\n{e}")
        return False

def guardar_egresos(poliza):
    app = None
    wb = None
    try:
        app = xw.App(visible=False)
        fecha_dt = datetime.strptime(poliza.fecha, "%d/%m/%Y")
        nombre_archivo = f"egresos_{fecha_dt.strftime('%b_%Y').lower()}.xlsx"
        ruta_descargas = os.path.join(config["carpeta_destino"], "PolizasDeEgresos")
        os.makedirs(ruta_descargas, exist_ok=True)
        ruta_archivo = os.path.join(ruta_descargas, nombre_archivo)

        if os.path.exists(ruta_archivo):
            wb = app.books.open(ruta_archivo)
        else:
            wb = app.books.open(ruta_absoluta("assets/plantillas/egresos.xlsx"))

        nombre_hoja = obtener_nombre_hoja(poliza.no_poliza)
        nombres_hojas = [sheet.name for sheet in wb.sheets]

        if nombre_hoja not in nombres_hojas:
            nombre_plantilla = "01 ene 2025"
            if nombre_plantilla in nombres_hojas:
                hoja_plantilla = wb.sheets[nombre_plantilla]
                hoja_nueva = hoja_plantilla.copy(after=wb.sheets[-1])
                hoja_nueva.name = nombre_hoja
            else:
                hoja_nueva = wb.sheets.add(nombre_hoja)
        hoja = wb.sheets[nombre_hoja]
        
        nombre_hoja = obtener_nombre_hoja(poliza.no_poliza)
        hoja = reemplazar_hoja_si_existe(wb, nombre_hoja)


        asignar_valores_en_hoja(hoja, poliza)

        if not insertar_entradas_en_hoja(hoja, poliza.conceptos):
            return

        wb.save(ruta_archivo)
        messagebox.showinfo("Éxito", f"Archivo guardado en: {ruta_archivo}")
    except Exception as e:
        print("Error al guardar:", e)
        traceback.print_exc()
        messagebox.showerror("Error", f"No se pudo guardar la información.\n{e}")
    finally:
        if wb is not None:
            wb.close()
        if app is not None:
            app.quit()

                
def guardar_pdf(poliza):
    app = None
    wb = None
    try:
        if not validar_campos_obligatorios_obj(poliza):
            return
        app = xw.App(visible=False)
        wb = app.books.open(ruta_absoluta("assets/plantillas/egresos.xlsx"))
        hoja = wb.sheets["01 ene 2025"]

        asignar_valores_en_hoja(hoja, poliza)

        if not insertar_entradas_en_hoja(hoja, poliza.conceptos):
            return

        fecha_actual = obtener_fecha_actual().replace("/", "-")
        nombre_archivo = f"Poliza_Egresos_{fecha_actual}.pdf"
        ruta_descargas = os.path.join(config["carpeta_destino"], "PolizasDeEgresos")
        os.makedirs(ruta_descargas, exist_ok=True)
        ruta_pdf = os.path.join(ruta_descargas, nombre_archivo)

        hoja.api.ExportAsFixedFormat(0, ruta_pdf)
        messagebox.showinfo("Éxito", f"PDF guardado en: {ruta_pdf}")
    except Exception as e:
        print("Error al exportar PDF:", e)
        traceback.print_exc()
        messagebox.showerror("Error", f"No se pudo exportar como PDF.\n{e}")
    finally:
        if wb is not None:
            wb.close()
        if app is not None:
            app.quit()
            
def reemplazar_hoja_si_existe(wb, nombre_hoja, nombre_plantilla="01 ene 2025"):
    nombres_existentes = [sheet.name for sheet in wb.sheets]

    # Si ya existe la hoja, elimínala
    if nombre_hoja in nombres_existentes:
        hoja_existente = wb.sheets[nombre_hoja]
        hoja_existente.delete()

    # Si existe la hoja plantilla, la copiamos
    if nombre_plantilla in nombres_existentes:
        hoja_plantilla = wb.sheets[nombre_plantilla]
        hoja_nueva = hoja_plantilla.copy(after=wb.sheets[-1])
        hoja_nueva.name = nombre_hoja
    else:
        # Si no hay plantilla, crear hoja en blanco
        hoja_nueva = wb.sheets.add(name=nombre_hoja)

    return hoja_nueva

