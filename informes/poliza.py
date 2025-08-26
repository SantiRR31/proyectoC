import traceback
from utils.config_utils import cargar_config
from utils.egresos_utils import validar_campos_obligatorios_obj
import xlwings as xw
from datetime import datetime
from tkinter import messagebox
import os
from utils.rutas import ruta_absoluta
from utils.utils import obtener_fecha_actual, obtener_nombre_hoja
from db.egresosDB import consultar_poliza_por_no, obtener_numeros_polizas_por_mes
from models.egresomodelos import *
import customtkinter as ctk
import threading
from time import sleep
import re 

config = cargar_config()

meses = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def asignar_valores_en_hoja(hoja, poliza):
    campos_a_celdas = {
        "fecha": "AQ8",
        "no_poliza": "AX5",
        "nombre": "A9",
        "monto": "AO9",
        "monto_letra": "A10",
        "tipo_pago": "T12",
        "clave_ref": "A13",
        "observaciones": "A47",
    }

    for campo, celda in campos_a_celdas.items():
        valor = getattr(poliza, campo, "") or ""
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
        hoja.range(celda).value = valor
        
         # Agregar firmas
        firmas = config.get("firmas", {})

        hoja.range("A55").value = firmas.get("elaboro", "")
        hoja.range("R55").value = firmas.get("reviso", "")
        hoja.range("AM55").value = firmas.get("autorizo", "")

def insertar_entradas_en_hoja(hoja, conceptos, mensaje=True):
    fila_inicial = 18
    fila_final = 38
    try:
        partidas_sumadas = {}
        for i, concepto in enumerate(conceptos, start=1):
            if not concepto.clave_cucop or not concepto.cargo:
                if mensaje:
                    messagebox.showerror("Error", f"Faltan datos en el concepto #{i}. Verifica que todos los campos estén completos.")
                return False
            clave = concepto.clave_cucop
            if clave not in partidas_sumadas:
                partidas_sumadas[clave] = {"total": 0}
            partidas_sumadas[clave]["total"] += float(concepto.cargo)

        total_filas_disponibles = fila_final - fila_inicial + 1
        total_partidas = len(partidas_sumadas)
        necesita_filas_con_espacios = (total_partidas - 1)
        espacio_requerido = total_partidas + necesita_filas_con_espacios

        usar_espacios = espacio_requerido <= total_filas_disponibles
        filas_necesarias = espacio_requerido if usar_espacios else total_partidas
        filas_vacias_arriba = (total_filas_disponibles - filas_necesarias) // 2
        fila_actual = fila_inicial + filas_vacias_arriba

        for partida, datos in partidas_sumadas.items():
            hoja.range(f"B{fila_actual}").value = partida
            hoja.range(f"AV{fila_actual}").value = datos["total"]
            fila_actual += 2 if usar_espacios else 1

        return True
    except Exception as e:
        print("Error al insertar entradas en la hoja:", e)
        if mensaje:
            messagebox.showerror("Error", f"No se pudieron insertar los conceptos.\n{e}")
        return False

def reemplazar_hoja_si_existe(wb, nombre_hoja, nombre_plantilla="01 ene 2025"):
    nombres_existentes = [sheet.name for sheet in wb.sheets]
    if nombre_hoja in nombres_existentes:
        wb.sheets[nombre_hoja].delete()
    if nombre_plantilla in nombres_existentes:
        hoja_plantilla = wb.sheets[nombre_plantilla]
        hoja_nueva = hoja_plantilla.copy(after=wb.sheets[-1])
        hoja_nueva.name = nombre_hoja
    else:
        hoja_nueva = wb.sheets.add(name=nombre_hoja)
    return hoja_nueva

def guardar_egresos(poliza, mensaje=True):
    app = None
    wb = None
    try:
        app = xw.App(visible=False)
        fecha_dt = datetime.strptime(poliza.fecha, "%d/%m/%Y")
        mes_texto = meses[fecha_dt.month]
        nombre_archivo = f"{mes_texto} {fecha_dt.year}.xlsx"
        ruta_descargas = os.path.join(config["carpeta_destino"], "Polizas De Egresos")
        os.makedirs(ruta_descargas, exist_ok=True)
        ruta_archivo = os.path.join(ruta_descargas, nombre_archivo)

        try:
            wb = app.books.open(ruta_archivo)
        except Exception as e:
            if "sólo lectura" in str(e).lower() or "read-only" in str(e).lower():
                if mensaje:
                    messagebox.showerror("Archivo en uso", f"No se puede guardar el informe porque el archivo está abierto en Excel.\n\nCierra:\n{ruta_archivo}")
                return
            wb = app.books.open(ruta_absoluta("assets/plantillas/egresos.xlsx"))

        nombre_hoja = obtener_nombre_hoja(poliza.no_poliza)
        hoja = reemplazar_hoja_si_existe(wb, nombre_hoja)

        asignar_valores_en_hoja(hoja, poliza)

        if not insertar_entradas_en_hoja(hoja, poliza.conceptos, mensaje=mensaje):
            wb.close()
            return

        wb.save(ruta_archivo)
        if mensaje:
            messagebox.showinfo("Éxito", f"Archivo guardado en: {ruta_archivo}")

    except Exception as e:
        print("Error al guardar:", e)
        traceback.print_exc()
        if mensaje:
            messagebox.showerror("Error", f"No se pudo guardar la información.\n{e}")

    finally:
        if wb is not None:
            wb.close()
        if app is not None:
            app.quit()

def esta_archivo_en_uso(ruta):
    try:
        os.rename(ruta, ruta)
        return False
    except OSError:
        return True

def guardar_pdf(poliza):
 
    app = None
    wb = None
    try:
        if not validar_campos_obligatorios_obj(poliza):
            return

        app = xw.App(visible=False)
        wb = app.books.open(ruta_absoluta("assets/plantillas/egresos.xlsx"))
        hoja = reemplazar_hoja_si_existe(wb, "TEMPORAL_PDF", nombre_plantilla="01 ene 2025")
        hoja.activate()  # Activar la hoja antes de exportar
        print("poliza.no_poliza:", poliza.no_poliza)
        no_poliza_limpio = poliza.no_poliza.replace("/", "-")
        nombre_archivo = f"poliza{no_poliza_limpio}.pdf"
        print("nombre del archivo: ", nombre_archivo)
        nombre_archivo = re.sub(r'[<>:"/\\|?*]', '', nombre_archivo)  
        ruta_pdf_dir = os.path.join(config["carpeta_destino"], "PDF", "PolizasEgresos")
        os.makedirs(ruta_pdf_dir, exist_ok=True)
        ruta_pdf = os.path.join(ruta_pdf_dir, nombre_archivo)
        
        if os.path.exists(ruta_pdf):
            if esta_archivo_en_uso(ruta_pdf):
                messagebox.showerror("Archivo en uso", f"No se puede exportar el PDF porque está abierto:\n{ruta_pdf}")
                return
            else:
                os.remove(ruta_pdf)
                sleep(0.2) 
                
        asignar_valores_en_hoja(hoja, poliza)

        if not insertar_entradas_en_hoja(hoja, poliza.conceptos, mensaje=True):
            wb.close()
            return

        hoja.api.ExportAsFixedFormat(0, ruta_pdf)
        respuesta = messagebox.askyesno("PDF exportado", f"PDF guardado en:\n{ruta_pdf}\n\n¿Deseas abrir la carpeta?")
        if respuesta:
            os.startfile(os.path.dirname(ruta_pdf))
    except Exception as e:
        print("Error al exportar PDF:", e)
        traceback.print_exc()
        messagebox.showerror("Error", f"No se pudo exportar como PDF.\n{e}")

    finally:
        if wb is not None:
            wb.close()
        if app is not None:
            app.quit()

def guardar_polizas_mes(parent, mes, anio):
    ventana = ctk.CTkToplevel(parent)
    ventana.title("Guardando pólizas")
    ventana.geometry("400x120")
    ventana.resizable(False, False)

    texto_estado = ctk.CTkLabel(ventana, text="Iniciando...", anchor="w")
    texto_estado.pack(pady=(15, 5), padx=20, fill="x")

    barra = ctk.CTkProgressBar(ventana, width=360)
    barra.pack(pady=10)
    barra.set(0)

    alive = True  # Control para saber si la ventana sigue activa

    def actualizar_ui(valor, texto):
        # Verificar si ventana y barra siguen existiendo antes de actualizar
        try:
            if ventana.winfo_exists() and barra.winfo_exists():
                barra.set(valor)
                texto_estado.configure(text=texto)
        except Exception:
            pass  # Ignorar si ya no existen (por cierre ventana)

    def tarea_guardado():
        nonlocal alive
        try:
            no_polizas = obtener_numeros_polizas_por_mes(mes, anio)
            total = len(no_polizas)
            if total == 0:
                parent.after(0, lambda: (
                    ventana.destroy(),
                    messagebox.showinfo("Sin datos", "No hay pólizas en ese mes.")
                ))
                alive = False
                return

            for i, no_poliza in enumerate(no_polizas):
                if not alive:
                    break
                poliza = consultar_poliza_por_no(no_poliza)
                guardar_egresos(poliza, mensaje=False)
                progreso = (i + 1) / total
                texto = f"Póliza {no_poliza} guardada ({i + 1}/{total})"
                parent.after(0, lambda p=progreso, t=texto: actualizar_ui(p, t))

            if alive:
                parent.after(0, lambda: (
                    ventana.destroy(),
                    messagebox.showinfo("Éxito", f"Se guardaron {total} pólizas.")
                ))
                alive = False

        except Exception as e:
            if alive:
                parent.after(0, lambda: (
                    ventana.destroy(),
                    messagebox.showerror("Error", str(e))
                ))
                alive = False

    # Si quieres puedes capturar evento de cerrar ventana para interrumpir hilo:
    def on_close():
        nonlocal alive
        alive = False
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", on_close)

    import threading
    threading.Thread(target=tarea_guardado, daemon=True).start()

