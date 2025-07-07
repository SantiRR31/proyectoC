from datetime import time
from datetime import datetime
import gc
import os
import sqlite3
import traceback
import xlwings as xw
from tkinter import messagebox, ttk
from utils.utils import *
from utils.rutas import ruta_absoluta
import customtkinter as ctk
import math
from db.egresosDB import *
from models.egresomodelos import *
from datetime import datetime
from utils.config_utils import cargar_config
from xlwings.utils import col_name
import re

config = cargar_config()

#----------------- Funciones de captura y validación de pólizas de egresos -----------------

def capturar_poliza(form, entradas):
    poliza_id = form["poliza_id"].get()
    fecha = form["fecha"].get()
    nombre = form["nombre"].get()
    monto = form["cargo"].get()
    montoletr = form["cargo_letras"].get()
    tipo_pago = form["tipo_pago"].get()
    clave_ref = form["clave_rastreo"].get()
    denominacion = form["denominacion"].get()
    observaciones = form["observaciones"].get()
    no_cheque = None
    if tipo_pago == "CHEQUE":
        no_cheque = form["no_cheque"].get().strip() or None  
    elif tipo_pago == "TRANSFERENCIA":
        clave_ref = form["clave_rastreo"].get().strip() or None

    poliza = PolizaEgreso(
        poliza_id,
        fecha,
        monto,
        montoletr,
        nombre,
        tipo_pago,
        clave_ref,
        denominacion,
        observaciones,
        no_cheque
    )

    total_conceptos = 0.0
    for entrada_clave, entrada_desc, entrada_importe in entradas:
        clave = entrada_clave.get().strip()
        descripcion = entrada_desc.get()
        try:
            partida_especifica = obtener_partida_especifica_por_clave(int(clave))
            cargo = float(entrada_importe.get())
        except ValueError:
            continue  # Ignora filas incompletas o con error
        if clave and descripcion and cargo:
            concepto = ConceptoEgreso(clave, descripcion, partida_especifica, cargo)
            poliza.agregar_concepto(concepto)
            total_conceptos += cargo

    try:
        monto_float = float(monto)
    except ValueError:
        from tkinter import messagebox
        messagebox.showerror("Error", "El monto general no es válido.")
        return None

    if abs(monto_float - total_conceptos) > 0.01:
        from tkinter import messagebox
        messagebox.showerror(
            "Totales no coinciden",
            "El monto total de los conceptos no coincide con el monto general.\nPor favor verifica los datos."
        )
        return None

    return poliza 


def validar_campos_obligatorios_obj(poliza):
    faltantes = poliza.campos_faltantes()
    
    if faltantes:
        mensaje = "msg de validar_campos_obligatorios_obj: Por favor complete los siguientes campos obligatorios:\n\n" + "\n".join(faltantes)
        messagebox.showerror("Campos incompletos", mensaje)
        return False
    return True

def obtener_valores_campos(form):
    return {
        "fecha": form["fecha"].get(),
        "no_poliza": form["no_poliza"].get(),
        "nombre": form["nombre"].get(),
        "cargo": form["cargo"].get(),
        "cargo_letras": form["cargo_letras"].get(),
        "tipo_pago": form["tipo_pago"].get(),
        "clave_rastreo": form["clave_rastreo"].get(),
        "denominacion": form["denominacion"].get(),
        "observaciones": form["observaciones"].get(),
    }

#------------------ Funciones de asignación y guardado de pólizas de egresos formatos pdf y -----------------

def asignar_valores_en_hoja(hoja, poliza):
    campos_a_celdas = {
        "fecha": "AQ8",
        "poliza_id": "AX5",
        "nombre": "A9",
        "monto": "AO9",
        "montoletr": "A10",
        "tipo_pago": "T12",
        "clave_ref": "A13",
        "denominacion": "A44",
        "observaciones": "A47",
    }

    for campo, celda in campos_a_celdas.items():
        valor = getattr(poliza, campo, "")
        if campo == "clave_ref":
            if poliza.tipo_pago == "CHEQUE":
                valor = f"NO. DE CHEQUE {poliza.no_cheque or ''}"
            elif poliza.tipo_pago == "TRANSF. ELECTRÓNICA":                valor = f"CLAVE DE RASTREO {poliza.clave_ref or ''}"
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
    try:
        app = xw.App(visible=False)
        # Archivo por mes
        fecha_dt = datetime.strptime(poliza.fecha, "%d/%m/%Y")
        nombre_archivo = f"egresos_{fecha_dt.strftime('%b_%Y').lower()}.xlsx"
        ruta_descargas = os.path.join(config["carpeta_destino"], "PolizasDeEgresos")
        os.makedirs(ruta_descargas, exist_ok=True)
        ruta_archivo = os.path.join(ruta_descargas, nombre_archivo)

        # Si el archivo existe, ábrelo; si no, crea uno nuevo desde la plantilla
        if os.path.exists(ruta_archivo):
            wb = xw.Book(ruta_archivo)
        else:
            wb = app.books.open(ruta_absoluta("assets/plantillas/egresos.xlsx"))

        nombre_hoja = obtener_nombre_hoja(poliza.poliza_id)
        nombres_hojas = [sheet.name for sheet in wb.sheets]
        if nombre_hoja not in nombres_hojas:
            # Copia la hoja plantilla (ajusta el nombre según tu plantilla)
            nombre_plantilla = "01 ene 2025"  # o el nombre real de tu hoja plantilla
            if nombre_plantilla in nombres_hojas:
                hoja_plantilla = wb.sheets[nombre_plantilla]
                hoja_nueva = hoja_plantilla.copy(after=wb.sheets[-1])
                hoja_nueva.name = nombre_hoja
            else:
                # Si no hay plantilla, crea una hoja en blanco como fallback
                hoja_nueva = wb.sheets.add(nombre_hoja)
        hoja = wb.sheets[nombre_hoja]
        asignar_valores_en_hoja(hoja, poliza)

        if not insertar_entradas_en_hoja(hoja, poliza.conceptos):
            wb.close()
            return

        wb.save(ruta_archivo)
        messagebox.showinfo("Éxito", f"Archivo guardado en: {ruta_archivo}")
        wb.close()
    except Exception as e:
        print("Error al guardar:", e)
        messagebox.showerror("Error", f"No se pudo guardar la información.\n{e}")
        traceback.print_exc()
    finally:
        if wb is not None:
            wb.close()
        if app is not None:
            app.quit()
                
def guardar_pdf(poliza):
    try:
        if not validar_campos_obligatorios_obj(poliza):
            return
        app = xw.App(visible=False)
        wb = app.books.open(ruta_absoluta("assets/plantillas/egresos.xlsx"))
        hoja = wb.sheets["01 ene 2025"]
        
        asignar_valores_en_hoja(hoja, poliza)

        if not insertar_entradas_en_hoja(hoja, poliza.conceptos):
            wb.close()
            return

        fecha_actual = obtener_fecha_actual().replace("/", "-")
        nombre_archivo = f"Poliza_Egresos_{fecha_actual}.pdf"
        ruta_descargas = os.path.expanduser(config["carpeta_destino"],"PolizasDeEgresos")
        os.makedirs(ruta_descargas, exist_ok=True)
        ruta_pdf = os.path.join(ruta_descargas, nombre_archivo)

        hoja.api.ExportAsFixedFormat(0, ruta_pdf)  # 0 = PDF
        wb.close()
        messagebox.showinfo("Éxito", f"PDF guardado en: {ruta_pdf}")
    except Exception as e:
        print("Error al exportar PDF:", e)
        messagebox.showerror("Error", f"No se pudo exportar como PDF.\n{e}")
        
#------------------ Animación de descarga y guardado -----------------

class AnimacionDescarga(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Descargando...")
        self.geometry("260x180")
        self.resizable(False, False)
        self.configure(fg_color="#191919")
        self.overrideredirect(True)  # Sin barra de título

        self.canvas = ctk.CTkCanvas(self, width=80, height=80, bg="#191919", highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.35, anchor="center")

        self.texto = ctk.CTkLabel(self, text="Descargando", font=("Arial", 16, "bold"), text_color="#3b82f6", fg_color="transparent")
        self.texto.place(relx=0.5, rely=0.7, anchor="center")
                # Centrar respecto a la ventana principal (master)
        if master is not None:
            self.update_idletasks()
            pantalla_w = self.winfo_screenwidth()
            pantalla_h = self.winfo_screenheight()
            win_w = 260
            win_h = 180
            x = (pantalla_w // 2) - (win_w // 2)
            y = (pantalla_h // 2) - (win_h // 2) - 30  # pequeño ajuste visual
            self.geometry(f"{win_w}x{win_h}+{x}+{y}")

        self.puntos = 0
        self.angulo = 0
        self.animar()

    def animar(self):
        self.canvas.delete("all")
        # Dibuja un círculo giratorio 
        radio = 30
        cx, cy = 40, 40
        for i in range(12):
            ang = math.radians(self.angulo + i * 30)
            x = cx + radio * math.cos(ang)
            y = cy + radio * math.sin(ang)
            color = "#3b82f6" if i == 0 else "#64748b"
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline=color)
        self.angulo = (self.angulo + 30) % 360

        # Texto animado "Descargando..."
        puntos = "." * (self.puntos % 4)
        self.texto.configure(text=f"Descargando{puntos}")
        self.puntos += 1

        self.after(120, self.animar)

def ejecutar_con_loading(funcion, btn_guardar, btn_descargar, contenedor_principal, limpiar_formulario, *args):
    if btn_guardar is not None:
        btn_guardar.configure(state="disabled", text="Guardando...")
    if btn_descargar is not None:
        btn_descargar.configure(state="disabled", text="Descargando...")

    # Mostrar animación visual
    anim = AnimacionDescarga(contenedor_principal)
    anim.grab_set()  # Hace modal la ventana de animación

    def ejecutar():
        try:
            resultado = funcion(*args)
            if resultado:
                messagebox.showinfo("Éxito", "Poliza Guardada correctamente")
            respuesta = messagebox.askyesno(
                "Nuevo documento",
                "¿Desea crear una nueva póliza?"
            )
            if respuesta:
                limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la información.\n{e}")
        finally:
            anim.destroy()  # Cierra la animación
            if btn_guardar is not None:
                btn_guardar.configure(state="normal", text="💾 Guardar")
            if btn_descargar is not None:
                btn_descargar.configure(state="normal", text="📥 Descargar")
    contenedor_principal.after(100, ejecutar)
    
    
def mostrar_loading_y_ejecutar(funcion, contenedor_principal, *args, **kwargs):
        
    anim = AnimacionDescarga(contenedor_principal)
    anim.grab_set()

    def ejecutar():
        try:
            funcion(*args, **kwargs)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")
        finally:
            anim.destroy()

    contenedor_principal.after(100, ejecutar)
    
#------------------ Funciones de limpieza y animación de confirmación -----------------
    
def limpiar_formulario(contenedor_principal, mostrar_formulario_egresos, frame_padre):
    respuesta = messagebox.askyesno(
        "Limpiar formulario",
        "¿Está seguro de limpiar el formulario?\nEsta acción no se puede deshacer.",
        icon="warning"
    )
    if respuesta:
        for widget in contenedor_principal.winfo_children():
            widget.destroy()
        mostrar_formulario_egresos(frame_padre)
            
            
def animar_confirmacion(widget):
        """Animación de confirmación mejorada"""
        color_original = widget.cget("fg_color")
        try:
            widget.configure(fg_color="#10b981")
            time.sleep(0.3)
            if widget.winfo_exists():
                widget.configure(fg_color=color_original)
        except:
            pass

#------------------ Funciones de generación de números de póliza -----------------

def generar_no_poliza_para_fecha(fecha):
    # Detecta y convierte si la fecha viene en formato 'DD/MM/YYYY'
    if "/" in fecha:
        dt = datetime.strptime(fecha, "%d/%m/%Y")
    else:
        dt = datetime.strptime(fecha, "%Y-%m-%d")
    consecutivo = obtener_siguiente_no_poliza_mes(dt.strftime("%d/%m/%Y"))
    mes = dt.strftime("%b").lower()
    anio = dt.strftime("%Y")
    dia = dt.strftime("%d")
    return f"{consecutivo}/{mes}/{anio}"

# egresos_utils.py

def consultar_poliza(widgets, no_poliza):
    print("Consultando póliza...")
    poliza = consultar_poliza_por_no(no_poliza)
    if poliza is None:
        messagebox.showerror("No encontrado", "No se encontró la póliza.")
        return
    else :
        print(f"Póliza encontrada: ")
        print("No. Póliza:", poliza.poliza_id)
        print("Fecha:", poliza.fecha)
        print("Monto:", poliza.monto)
        print("Monto Letra:", poliza.montoletr)
        print("Nombre:", poliza.nombre)
        print("Tipo de pago:", poliza.tipo_pago)
        print("Clave/ref:", poliza.clave_ref)
        print("Denominación:", poliza.denominacion)
        print("Observaciones:", poliza.observaciones)
        print("No. Cheque:", poliza.no_cheque)
        print("Conceptos:")
    for concepto in poliza.conceptos:
        print("  ", concepto)
    
    for entry in widgets.get("entradas", []):
        entry.configure(state="normal")

# Asigna los valores a los campos del formulario
    widgets.entradas["poliza_id"].delete(0, "end")
    widgets.entradas["poliza_id"].insert(0, poliza.poliza_id)

    widgets.entradas["fecha"].set_date(poliza.fecha) # Si usas DateEntry con .set()

    widgets.entradas["nombre"].delete(0, "end")
    widgets.entradas["nombre"].insert(0, poliza.nombre)

    widgets.entradas["cargo"].delete(0, "end")
    widgets.entradas["cargo"].insert(0, poliza.monto)

    widgets.entradas["cargo_letras"].delete(0, "end")
    widgets.entradas["cargo_letras"].insert(0, poliza.montoletr)

    widgets.entradas["tipo_pago"].set(poliza.tipo_pago)

    widgets.entradas["clave_rastreo"].delete(0, "end")
    widgets["clave_rastreo"].insert(0, poliza.clave_ref or "")

    widgets.entradas["denominacion"].delete(0, "end")
    widgets.entradas["denominacion"].insert(0, poliza.denominacion or "")

    widgets.entradas["observaciones"].delete(0, "end")
    widgets.entradas["observaciones"].insert(0, poliza.observaciones or "")

    if "no_cheque" in widgets and widgets.entradas["no_cheque"]:
        widgets.entradas["no_cheque"].delete(0, "end")
        widgets.entradas["no_cheque"].insert(0, poliza.no_cheque or "")

def editar_poliza():
    print("Editando póliza...")

def eliminar_poliza():
    print("Eliminando póliza...")

def agregar_poliza():
    print("Agregando nueva póliza...")

def buscar_poliza():
    print("Buscando póliza...")
#------------------ Funciones de búsqueda y sugerencias -----------------
            
def mostrar_sugerencias(event, entrada_desc, entrada_clave, lista_sugerencias):
        tecla = event.keysym
        if tecla in ("Up", "Down", "Return", "Escape"):
            return
        texto = entrada_desc.get().strip()
        if len(texto) < 2:
            lista_sugerencias.place_forget()
            return 
        try:
            coincidencias = buscar_clave_por_descripcion(texto)
            lista_sugerencias.delete(0, tk.END)

            if coincidencias:
                for item in coincidencias[:10]:
                    texto_mostrado = f'{item ["clave"]} - {item["descripcion"][:50]}... (Partida: {item ["partida"]})'
                    lista_sugerencias.insert(tk.END, texto_mostrado)

                lista_sugerencias.place(
                    in_=entrada_desc,
                    relx=0,
                    rely=1.0,
                    relwidth=1.0,
                    bordermode="outside",
                )
                lista_sugerencias.lift()
            # Guardamos las coincidencias para uso posterior
                lista_sugerencias.coins = coincidencias
            else:
                lista_sugerencias.place_forget()
        except Exception as e:
            print(f"Error en sujerencias:{e} ")
            lista_sugerencias.place_forget()
            
def llenar_denominacion(event, entrada_clave, entrada_resultado):
        clave = entrada_clave.get()
        denominacion = buscar_descripcion_db(clave)
        entrada_resultado.configure(state="normal")
        entrada_resultado.delete(0, tk.END)
        entrada_resultado.insert(0, denominacion)
        #entrada_resultado.configure(state="readonly")
        
def llenar_por_clave(event, entrada_clave, entrada_desc):
    clave = entrada_clave.get().strip()
    if clave:
        try:
            descripcion = buscar_descripcion_db(clave)
            if descripcion and descripcion.strip().lower() != "No encontrada":                    
                entrada_desc.configure(state="normal", fg_color= "transparent")
                entrada_desc.delete(0, tk.END)
                entrada_desc.insert(0, descripcion)
                #threading.Thread(target=lambda: animar_confirmacion(entrada_desc), daemon=True).start()
            else:
                entrada_desc.configure(state="normal")                    
                entrada_desc.delete(0, tk.END)
                entrada_desc.insert(0, "No encontrada")
                entrada_desc.configure(fg_color="#ef8989")
 # rojo claro (bg)
        except Exception as e:
            print(f"Error al buscar descripción: {e}")
            
            
            
def actualizar_total(entradas, total_entry, cargo_entry, validacion_label, validacion_enty, total_ctk):
    try:
        suma_total = sum(float(entrada[2].get()) for entrada in entradas if entrada[2].get().strip())
        total_entry.configure(state="normal")
        total_entry.delete(0, tk.END)
        total_entry.insert(0, f"${suma_total:,.2f}")
        total_entry.configure(state="readonly")

        importe_valor = cargo_entry.get().strip()
        if importe_valor:
            importe_float = float(importe_valor)
            diferencia = abs(importe_float - suma_total)

            if diferencia < 0.01:
                validacion_label.configure(
                    text="✓ Totales coinciden",
                    text_color="#10b981",
                    font=("Arial", 10, "bold")
                )
                validacion_enty.configure(
                    border_color="#10b981"
                    )
                total_ctk.configure(
                    text_color="#10b981",
                    )
            else:
                validacion_label.configure(
                    text=f"✗ Diferencias (${diferencia:,.2f})",
                    text_color="#ef4444",
                    font=("Arial", 10, "bold")
                )
                validacion_enty.configure(
                    border_color="#ef4444"
                )
                total_ctk.configure(
                    text_color="#ef4444",
                )
        else:
            validacion_label.configure(
                text="⚠ Ingrese monto total",
                text_color="#f59e0b",
                font=("Arial", 10)
            )
            validacion_enty.configure(
                border_color="#f59e0b"
            )
            total_ctk.configure(
                text_color="#f59e0b",
            )
    except ValueError:
        validacion_label.configure(
            text="⚠ Valores no válidos",
            text_color="#f59e0b",
            font=("Arial", 10)
        )
        validacion_enty.configure(
            border_color="#f59e0b"
        )
        total_ctk.configure(
            text_color="#f59e0b",
        )

#------------------ Funciones de actualización de estado del formulario -----------------

def actualizar_estado_formulario(modo: str, widgets: dict, campos=None, conceptos=None, btn_guardar=None, btn_descargar=None, btn_buscar=None):
    desactivar = modo in ("Consultar", "Eliminar")

    for entry in widgets.get("entradas", []):
        # Si es el widget de No. de Póliza, siempre debe estar normal
        if entry == widgets.get("no_poliza", None) or entry._name == "no_poliza":
            entry.configure(state="normal")
        elif entry == widgets["entradas"][1]:  # Suponiendo que no_poliza es el segundo en la lista
            entry.configure(state="normal")
        else:
            entry.configure(state="normal" if not desactivar else "disabled")
            if isinstance(entry, ctk.CTkEntry):
                entry.configure(border_color="#3b82f6" if not desactivar else "#4b5563")

    for boton in widgets.get("botones", []):
        boton.configure(state="normal" if not desactivar else "disabled")
        if desactivar:
            boton.configure(fg_color="#6b7280")
        else:
            if boton.cget("text") == "💾 Guardar":
                boton.configure(fg_color="#10b981", hover_color="#059669")
            elif boton.cget("text") == "📥 Descargar":
                boton.configure(fg_color="#3b82f6", hover_color="#2563eb")
            elif boton.cget("text") == " Abrir Carpeta":
                boton.configure(fg_color="#6b7280", hover_color="#4b5563")
            else:
                boton.configure(fg_color="#1f6aa5", hover_color="#103858")

    for menu in widgets.get("menus", []):
        try:
            menu.configure(state="normal" if not desactivar else "disabled")
        except Exception:
            pass

    # Validar campos obligatorios en modo agregar/editar
    if modo in ("Agregar", "Editar"):
        if campos is not None and conceptos is not None and btn_guardar and btn_descargar and btn_buscar:
            actualizar_estado_botones(modo, campos, conceptos, btn_guardar, btn_descargar, btn_buscar)
            
def actualizar_estado_botones(modo, campos, conceptos, btn_guardar, btn_descargar, btn_buscar):
    # Determina el estado deseado según el modo y la validación
    if modo.lower() in ("agregar", "editar"):
        campos_vacios = campos_obligatorios_vacios(campos, conceptos)
        guardar_estado = "disabled" if campos_vacios else "normal"
        descargar_estado = "disabled" if campos_vacios else "normal"
        buscar_estado = "disabled" if modo.lower() == "agregar" else "normal"
    elif modo.lower() in ("consultar", "eliminar"):
        guardar_estado = "disabled"
        descargar_estado = "disabled"
        buscar_estado = "normal"
    else:
        guardar_estado = "normal"
        descargar_estado = "normal"
        buscar_estado = "normal"

    # Solo actualiza si el estado realmente cambia
    if btn_guardar.cget("state") != guardar_estado:
        btn_guardar.configure(state=guardar_estado)
    if btn_descargar.cget("state") != descargar_estado:
        btn_descargar.configure(state=descargar_estado)
    if btn_buscar.cget("state") != buscar_estado:
        btn_buscar.configure(state=buscar_estado)
        
        
def campos_obligatorios_vacios(campos, conceptos):
    # Valida los campos fijos
    if any(campo.get().strip() == "" for campo in campos):
        return True
    # Valida los conceptos (clave, descripción, importe)
    for entrada_clave, entrada_desc, entrada_importe in conceptos:
        if not entrada_clave.get().strip() or not entrada_desc.get().strip() or not entrada_importe.get().strip():
            return True
    return False

#------------------ Funciones para generar el liro de egresos -----------------

meses = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def confirmar_y_generar_egresos(contenedor_principal=None):
    ventana = ctk.CTkToplevel()
    ventana.title("Generar reporte de egresos")
    ventana.geometry("340x180")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.transient(contenedor_principal)

    meses_lista = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    hoy = datetime.now()
    mes_actual = hoy.month
    anio_actual = hoy.year

    ctk.CTkLabel(ventana, text="Seleccione el mes y año del reporte:", font=("Arial", 13)).pack(pady=(16, 6))

    frame = ctk.CTkFrame(ventana, fg_color="transparent")
    frame.pack(pady=4)

    mes_var = ctk.StringVar(value=meses_lista[mes_actual-1])
    anio_var = ctk.StringVar(value=str(anio_actual))

    mes_cb = ttk.Combobox(frame, values=meses_lista, textvariable=mes_var, state="readonly", width=14)
    mes_cb.grid(row=0, column=0, padx=8)
    anio_cb = ttk.Combobox(frame, values=[str(a) for a in range(anio_actual-5, anio_actual+2)], textvariable=anio_var, width=8, state="readonly")
    anio_cb.grid(row=0, column=1, padx=8)

    def generar_reporte_seleccionado():
        mes_idx = meses_lista.index(mes_var.get()) + 1
        anio = int(anio_var.get())
        mes_str = f"{anio}-{mes_idx:02d}"
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            lambda: generar_reporte_egresos_xlwings(mes_str),
            contenedor_principal=contenedor_principal,
        )

    def generar_reporte_actual():
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            generar_reporte_egresos_xlwings,
            contenedor_principal=contenedor_principal,
        )

    btn_frame = ctk.CTkFrame(ventana, fg_color="transparent")
    btn_frame.pack(pady=18)

    ctk.CTkButton(btn_frame, text="Generar mes seleccionado", command=generar_reporte_seleccionado, width=140).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Generar mes actual", command=generar_reporte_actual, width=120).pack(side="left", padx=10)

# función generar_reporte_egresos_
def generar_reporte_egresos_xlwings(mes_anio=None):
    app = None
    wb = None
    try:
        hoy = datetime.now()
        mes_actual = mes_anio if mes_anio else hoy.strftime('%Y-%m')
        nombre_hoja = hoy.strftime('%b %Y').lower()  # Ejemplo: 'jun 2025'

        polizas_mes = obtener_polizas_egresos_mes(mes_actual)
        if not polizas_mes:
            raise ValueError("No se encontraron pólizas de egresos en el mes actual.")

        partidas_mes = [row[0] for row in obtener_partidas_mes(mes_actual)]

        partidas_finales = [120, 330]
        # Filtra y ordena ascendente las demás
        partidas_ordenadas = sorted([p for p in partidas_mes if p not in partidas_finales])
        # Agrega al final las partidas especiales si existen en la lista
        partidas_ordenadas += [p for p in partidas_finales if p in partidas_mes]
        partidas_mes = partidas_ordenadas
        print(partidas_mes)

        # Abrir Excel de forma segura
        app = xw.App(visible=False)
        wb = app.books.open("assets/plantillas/LibroDeEgresos.xls")

        # Crear hoja si no existe
        nombre_hoja_plantilla = "mar 2025"
        if nombre_hoja not in [sheet.name.lower() for sheet in wb.sheets]:
            try:
                sht_plantilla = wb.sheets[nombre_hoja_plantilla]
                sht_nueva = sht_plantilla.copy(after=wb.sheets[-1])
                sht_nueva.name = nombre_hoja
            except Exception as e:
                raise ValueError(f"No se pudo crear la hoja '{nombre_hoja}': {e}")

        sht = wb.sheets[nombre_hoja]

        # Limpiar datos anteriores
        sht.range("A10:J40").clear_contents()

        # Encabezados
        mes_excel = hoy.strftime('%b-%y').lower()
        sht.range("T5").value = mes_excel
        sht.range("J5").value = config["no_cecati"]

        col_inicio = 4
        max_cols = 17
        columna_j = 10
        fila_formula = 47
        rango_inicio = 10
        rango_fin = 46

        num_partidas = len(partidas_mes)
        num_polizas = len(polizas_mes)

        # Insertar columnas si hay más partidas
        if num_partidas > max_cols:
            columnas_extra = num_partidas - max_cols
            for offset in range(columnas_extra):
                col_destino = columna_j + offset
                sht.range((1, col_destino)).api.EntireColumn.Insert()
                letra_col = xw.utils.col_name(col_destino)
                formula = f"=SUMA({letra_col}{rango_inicio}:{letra_col}{rango_fin})"
                sht.range((fila_formula, col_destino)).formula = formula

        # Escribir encabezados de partida
        for idx, partida in enumerate(partidas_mes):
            sht.range((8, col_inicio + idx)).value = partida

        # Insertar filas si hay más pólizas de las esperadas
        fila_inicio = 10
        if num_polizas > (rango_fin - rango_inicio + 1):
            filas_extra = num_polizas - (rango_fin - rango_inicio + 1)
            sht.range(f"A{rango_fin + 1}:A{rango_fin + filas_extra}").api.EntireRow.Insert()

        # Escribir datos de pólizas
        for idx, (fecha, no_poliza, id_poliza, tipo_pago, no_cheque) in enumerate(polizas_mes):
            fila = fila_inicio + idx
            fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
            sht.range(f"A{fila}").value = fecha_dt
            sht.range(f"B{fila}").value = no_poliza.split("/")[0] if no_poliza else ""
            sht.range(f"C{fila}").value = no_cheque if tipo_pago == "CHEQUE" else "TRANS" if tipo_pago == "TRANSF. ELECTRÓNICA" else ""

            cargos = obtener_conceptos_por_partida_especifica(id_poliza)
            for col_idx, partida in enumerate(partidas_mes):
                valor = cargos.get(partida, 0)
                sht.range((fila, col_inicio + col_idx)).value = "" if valor == 0 else valor

        # Guardar archivo en carpeta de salida
        carpeta_salida = os.path.join(config["carpeta_destino"], "InformesDeEgresos")
        os.makedirs(carpeta_salida, exist_ok=True)

        mes_act = hoy.month
        anio_act = hoy.year
        sht.name = f"{meses[mes_act]} {anio_act}"

        archivo_salida = os.path.join(carpeta_salida, f"egresos_{mes_actual}.xlsx")
        #app.visible = True
        wb.app.calculation = 'automatic'
        #sht.calculate()
        wb.app.calculate()
        wb.save(archivo_salida)

        # Confirmación
        
        messagebox.showinfo(
            "Reporte generado",
            "El reporte de egresos se ha generado exitosamente.\n\nAtención:\nEl archivo fue generado. Si ves #### en las celdas, abre el archivo en Excel y presiona F9 o guarda el archivo para recalcular las fórmulas."
        )

        return archivo_salida

    except Exception as e:
        print(f"Error generando el reporte de egresos: {e}")
        messagebox.showerror("Error", f"Ocurrió un error al generar el reporte de egresos:\n{e}")

    finally:
        # Limpieza segura de recursos
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

        # Liberar memoria
        wb = None
        app = None
        sht = None
        
        gc.collect()


def confirmar_y_generar_consolidado(contenedor_principal=None):
    ventana = ctk.CTkToplevel()
    ventana.title("Generar informe consolidado de egresos")
    ventana.geometry("340x180")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.transient(contenedor_principal)

    meses_lista = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    hoy = datetime.now()
    mes_actual = hoy.month
    anio_actual = hoy.year

    ctk.CTkLabel(ventana, text="Seleccione el mes y año del reporte:", font=("Arial", 13)).pack(pady=(16, 6))

    frame = ctk.CTkFrame(ventana, fg_color="transparent")
    frame.pack(pady=4)

    mes_var = ctk.StringVar(value=meses_lista[mes_actual-1])
    anio_var = ctk.StringVar(value=str(anio_actual))

    mes_cb = ttk.Combobox(frame, values=meses_lista, textvariable=mes_var, state="readonly", width=14)
    mes_cb.grid(row=0, column=0, padx=8)
    anio_cb = ttk.Combobox(frame, values=[str(a) for a in range(anio_actual-5, anio_actual+2)], textvariable=anio_var, width=8, state="readonly")
    anio_cb.grid(row=0, column=1, padx=8)

    def generar_reporte_seleccionado():
        mes_idx = meses_lista.index(mes_var.get()) + 1
        anio = int(anio_var.get())
        mes_str = f"{anio}-{mes_idx:02d}"
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            lambda: generar_informe_consolidado_egresos(mes_str),
            contenedor_principal=contenedor_principal,
        )

    def generar_reporte_actual():
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            generar_informe_consolidado_egresos,
            contenedor_principal=contenedor_principal,
        )

    btn_frame = ctk.CTkFrame(ventana, fg_color="transparent")
    btn_frame.pack(pady=18)

    ctk.CTkButton(btn_frame, text="Generar mes seleccionado", command=generar_reporte_seleccionado, width=140).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Generar mes actual", command=generar_reporte_actual, width=120).pack(side="left", padx=10)



def generar_informe_consolidado_egresos(mes_anio=None):
    app = None
    wb = None
    try:
        hoy = datetime.now()
        mes_actual = mes_anio if mes_anio else hoy.strftime('%Y-%m')
        # Extrae año y mes del string 'YYYY-MM'
        anio, mes = mes_actual.split('-')
        mes_nombre = meses[int(mes)]
        partidas_mes = obtener_partidas_mesagrupasa(mes_actual)  # Debe devolver (codigo, descripcion, total_cargo)
        
        # Abrir plantilla
        app = xw.App(visible=False)
        wb = app.books.open("assets/plantillas/ConsolidadoEgresos.xls")
        sht = wb.sheets[0]  # O el nombre de la hoja

        # Llenar datos generales
        sht.range("M5").value = f"CECATI No. {config['no_cecati']}"
        sht.range("R8").value = f"{mes_nombre} {anio}"
        sht.range("AH8").value = hoy.strftime("%d %m %Y")

        # Diccionario de rangos por grupo
        rangos = {
            2100: ("C14", "C20"),
            2200: ("C24", "C25"),
            2400: ("C29", "C37"),
            2500: ("C41", "C45"),
            2600: ("C49", "C51"),
            2700: ("C54", "C58"),
            2900: ("C61", "C67"),
            3100: ("R14", "R20"),
            3200: ("R23", "R23"),
            3300: ("R27", "R33"),
            3400: ("R37", "R40"),
            3500: ("R45", "R52"),
            3600: ("R55", "R55"),
            3700: ("R58", "R64"),
            3800: ("R67", "R69"),
            3900: ("R73", "R73"),
            4400: ("AG14", "AG15"),
            5100: ("AG22", "AG25"),
            5200: ("AG29", "AG32"),
            5300: ("AG36", "AG37"),
            5600: ("AG40", "AG44"),
            5900: ("AG48", "AG48"),
        }
        
        columnas_cargo = {
            2100: "H",
            2200: "H",
            2400: "H",
            2500: "H",
            2600: "H",
            2700: "H",
            2900: "H",
            3100: "W",
            3200: "W",
            3300: "W",
            3400: "W",
            3500: "W",
            3600: "W",
            3700: "W",
            3800: "W",
            3900: "W",
            4400: "AL",
            5100: "AL",
            5200: "AL",
            5300: "AL",
            5600: "AL",
            5900: "AL",
        }
        
        # Otros
        sht.range("Al59").value = obtener_total_deudores(mes_actual)
        sht.range("Al60").value = obtener_total_acreedores(mes_actual)

        # Agrupa partidas por grupo (2100, 2200, etc.)
        partidas_por_grupo = agrupar_partidas_por_grupo(partidas_mes)
        
        #print("Partidas por grupo:", partidas_por_grupo)
        
        carpeta_salida = os.path.join(config["carpeta_destino"], "Consolidado de egresos")
        os.makedirs(carpeta_salida, exist_ok=True)

        # Para cada grupo, coloca los códigos y cargos en las celdas correspondientes

        for grupo, (inicio, fin) in rangos.items():
            codigos = partidas_por_grupo.get(grupo, [])
            col = re.match(r'[A-Z]+', inicio).group()
            fila_inicio = int(re.search(r'\d+', inicio).group())
            col_cargo = columnas_cargo[grupo]
            for i, (codigo, total_cargo) in enumerate(codigos):
                if fila_inicio + i > int(re.search(r'\d+', fin).group()):
                    break
                celda_codigo = f"{col}{fila_inicio + i}"
                celda_cargo = f"{col_cargo}{fila_inicio + i}"
                try:
                    sht.range(celda_codigo).value = codigo
                    sht.range(celda_cargo).value = total_cargo
                except Exception as e:
                    print(f"Error al escribir en {celda_codigo} o {celda_cargo}: {e}")
                    raise
                
        # Guardar archivo
        archivo_salida = os.path.join(carpeta_salida, f"consolidado_egresos_{mes_actual}.xlsx")
        wb.save(archivo_salida)
        messagebox.showinfo("Reporte generado", f"El informe consolidado se ha generado:\n{archivo_salida}")
        return archivo_salida

    except Exception as e:
        print(f"Error generando el informe consolidado: {e}")
        messagebox.showerror("Error", f"Ocurrió un error al generar el informe consolidado:\n{e}")
    finally:
        if wb:
            wb.close()
        if app:
            app.quit()
        gc.collect()  
        
        


def confirmar_y_generar_infReal(contenedor_principal=None):
    ventana = ctk.CTkToplevel()
    ventana.title("Generar informe real de egresos")
    ventana.geometry("340x180")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.transient(contenedor_principal)

    meses_lista = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    hoy = datetime.now()
    mes_actual = hoy.month
    anio_actual = hoy.year

    ctk.CTkLabel(ventana, text="Seleccione el mes y año del reporte:", font=("Arial", 13)).pack(pady=(16, 6))

    frame = ctk.CTkFrame(ventana, fg_color="transparent")
    frame.pack(pady=4)

    mes_var = ctk.StringVar(value=meses_lista[mes_actual-1])
    anio_var = ctk.StringVar(value=str(anio_actual))

    mes_cb = ttk.Combobox(frame, values=meses_lista, textvariable=mes_var, state="readonly", width=14)
    mes_cb.grid(row=0, column=0, padx=8)
    anio_cb = ttk.Combobox(frame, values=[str(a) for a in range(anio_actual-5, anio_actual+2)], textvariable=anio_var, width=8, state="readonly")
    anio_cb.grid(row=0, column=1, padx=8)

    def generar_reporte_seleccionado():
        mes_idx = meses_lista.index(mes_var.get()) + 1
        anio = int(anio_var.get())
        mes_str = f"{anio}-{mes_idx:02d}"
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            lambda: generar_inf_real_egresos(mes_str),
            contenedor_principal=contenedor_principal,
        )

    def generar_reporte_actual():
        ventana.destroy()
        mostrar_loading_y_ejecutar(
            generar_inf_real_egresos,
            contenedor_principal=contenedor_principal,
        )

    btn_frame = ctk.CTkFrame(ventana, fg_color="transparent")
    btn_frame.pack(pady=18)

    ctk.CTkButton(btn_frame, text="Generar mes seleccionado", command=generar_reporte_seleccionado, width=140).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Generar mes actual", command=generar_reporte_actual, width=120).pack(side="left", padx=10)

        
def generar_inf_real_egresos(mes_anio=None):
    app = None
    wb = None
    try:
        hoy = datetime.now()
        mes_actual = mes_anio if mes_anio else hoy.strftime()
        anio, mes = mes_actual.split('-')
        mes_nombre = meses[int(mes)]
        partidas_mes = obtener_partidas_mesagrupasa(mes_actual)
        
        app = xw.App(visible=False)
        wb = app.books.open("assets/plantillas/InformeReal.xls")
        sht = wb.sheets[0]
        
        # llenar datos generales
        sht.range("AI5").value = config["clave_cecati"] #clave del cecati
        sht.range("AQ5").value = hoy.strftime("%d %m %Y") # Fecha de elaboracion 
        sht.range("AX5").value = f"{mes_nombre} {anio}" # Periodo de infrome 
        sht.range("BB1").value = config["no_cecati"] #no cecati 
        
        # agrupar partidas por grupo: 
        partidas_por_grupo = agrupar_partidas_por_grupo(partidas_mes)
        
        print ("partidasporgrupo",partidas_por_grupo)
        
        fila = 12
        for grupo in sorted(partidas_por_grupo.keys()):
            if grupo in (100,300):
                continue
            partidas = partidas_por_grupo[grupo]
            sht.range(f"B{fila}").value = grupo  # Escribe el grupo solo una vez
            fila += 1
            for codigo, total in partidas:
                if codigo in (120, 330):
                    continue
                sht.range(f"B{fila}").value = codigo  # Ahora sí, la partida específica
                sht.range(f"AQ{fila}").value = total
                fila += 1
        total_120 = None
        total_330 = None
        if 100 in partidas_por_grupo:
            for codigo, total in partidas_por_grupo[100]:
                if codigo == 120:
                    total_120 = total
        if 330 in partidas_por_grupo:
            for codigo, total in partidas_por_grupo[330]:
                if codigo == 330:
                    total_330 = total
        # Si 120 viene como partida suelta (no agrupada en 100)
        if total_120 is None:
            for grupo, partidas in partidas_por_grupo.items():
                for codigo, total in partidas:
                    if codigo == 120:
                        total_120 = total
        if total_330 is None:
            for grupo, partidas in partidas_por_grupo.items():
                for codigo, total in partidas:
                    if codigo == 330:
                        total_330 = total

        if total_120 is not None:
            sht.range("AQ49").value = total_120
        if total_330 is not None:
            sht.range("AQ50").value = total_330
        
        archivo_salida = os.path.join(config["carpeta_destino"], f"InformeReal_{mes_actual}.xlsx")
        wb.save(archivo_salida)
        messagebox.showinfo("Reporte generado", f"El informe real se ha generado:\n{archivo_salida}")
        return archivo_salida
    except Exception as e:
        print(f"Error generando el informe real de egresos:{e}")
        messagebox.showerror("Error", f"Ocurrió un error al generar el informe real:\n{e}")
        
    finally:
        if wb:
            wb.close()
        if app:
            app.quit()
        gc.collect()
        
        
    