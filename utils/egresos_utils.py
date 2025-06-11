from datetime import time
from datetime import datetime
import os
import xlwings as xw
from tkinter import messagebox
from utils.utils import obtener_fecha_actual
from utils.rutas import ruta_absoluta
import customtkinter as ctk
import math
from db.egresosDB import *
from models.egresomodelos import *
from datetime import datetime
import tkinter as tk

#----------------- Funciones de captura y validación de pólizas de egresos -----------------
def capturar_poliza(form,entradas):
        poliza_id = form["poliza_id"].get()
        fecha = form["fecha"].get()
        nombre = form["nombre"].get()
        monto = form["cargo"].get()
        montoletr = form["cargo_letras"].get()
        tipo_pago = form["tipo_pago"].get()
        clave_ref = form["clave_rastreo"].get()
        denominacion = form["denominacion"].get()
        observaciones = form["observaciones"].get()
        
        poliza = PolizaEgreso(
            poliza_id,
            fecha,  
            monto,
            montoletr,
            nombre, 
            tipo_pago,
            clave_ref,
            denominacion,
            observaciones
        )

        for entrada_clave, entrada_desc, entrada_importe in entradas:
            clave = entrada_clave.get().strip()
            #print(f"Advertencia: clave VALOR '{clave}'")
            descripcion = entrada_desc.get()
            partida_especifica = obtener_partida_especifica_por_clave(int(clave))
            cargo = float(entrada_importe.get())
            if clave and descripcion and cargo:
                concepto = ConceptoEgreso(clave, descripcion, partida_especifica, cargo)
                poliza.agregar_concepto(concepto)
                
        return poliza 


def validar_campos_obligatorios_obj(poliza):
    faltantes = poliza.campos_faltantes()
    if faltantes:
        mensaje = "Por favor complete los siguientes campos obligatorios:\n\n" + "\n".join(faltantes)
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
        if campo == "clave_rastreo":
            valor = f"CLAVE DE RASTREO {valor}"
        hoja.range(celda).value = valor

def insertar_entradas_en_hoja(hoja, conceptos, fila_inicial=18):
    for concepto in conceptos:
        if concepto.partida_especifica and concepto.cargo:
            hoja.range(f"B{fila_inicial}").value = concepto.partida_especifica
            hoja.range(f"AV{fila_inicial}").value = float(concepto.cargo)
            fila_inicial += 1
        else:
            messagebox.showerror("Error", "Faltan datos. Verifica que todos los campos estén completos.")
            return False
    return True

def guardar_egresos(poliza):
    try:
        app = xw.App(visible=False)
        wb = app.books.open(ruta_absoluta("assets/plantillas/egresos.xlsx"))
        hoja = wb.sheets["01 ene 2025"]
        asignar_valores_en_hoja(hoja, poliza)

        if not insertar_entradas_en_hoja(hoja, poliza.conceptos):
            wb.close()
            return

        fecha_actual = obtener_fecha_actual().replace("/", "-")
        nombre_archivo = f"Poliza_Egresos_{fecha_actual}.xlsx"
        ruta_descargas = os.path.expanduser("~/Documentos/Cecati122/PolizasDeEgresos")
        os.makedirs(ruta_descargas, exist_ok=True)
        ruta_archivo = os.path.join(ruta_descargas, nombre_archivo)

        wb.save(ruta_archivo)
        messagebox.showinfo("Éxito", f"Archivo guardado en: {ruta_archivo}")
        wb.close()
    except Exception as e:
        print("Error al guardar:", e)
        messagebox.showerror("Error", f"No se pudo guardar la información.\n{e}")
                
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
        ruta_descargas = os.path.expanduser("~/Documentos/Cecati122/PolizasDeEgresos")
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
    btn_guardar.configure(state="disabled", text="Guardando...")
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
            btn_guardar.configure(state="normal", text="💾 Guardar")
            btn_descargar.configure(state="normal", text="📥 Descargar")
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

def consultar_poliza():
    print("Consultando póliza...")

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
            
            
            
def actualizar_total(entradas, total_entry, cargo_entry, validacion_label):
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
            else:
                validacion_label.configure(
                    text=f"✗ Diferencias (${diferencia:,.2f})",
                    text_color="#ef4444",
                    font=("Arial", 10, "bold")
                )
        else:
            validacion_label.configure(
                text="⚠ Ingrese monto total",
                text_color="#f59e0b",
                font=("Arial", 10)
            )
    except ValueError:
        validacion_label.configure(
            text="⚠ Valores no válidos",
            text_color="#f59e0b",
            font=("Arial", 10)
        )

#------------------ Funciones de actualización de estado del formulario -----------------

def actualizar_estado_formulario(modo: str, widgets: dict, campos=None, conceptos=None, btn_guardar=None, btn_descargar=None, btn_buscar=None):
    desactivar = modo in ("Consultar", "Eliminar")

    for entry in widgets.get("entradas", []):
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
                boton.configure(fg_color="#22c55e", hover_color="#16a34a")

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
    # Por defecto, todos los botones activos
    guardar_estado = "normal"
    descargar_estado = "normal"
    buscar_estado = "normal"

    # En modo agregar o editar, desactiva si hay campos vacíos
    if modo in ("agregar", "editar"):
        if campos_obligatorios_vacios(campos, conceptos):
            guardar_estado = "disabled"
            descargar_estado = "disabled"
        # Solo en modo agregar, desactiva buscar
        if modo == "agregar":
            buscar_estado = "disabled"
    # En modo consultar o eliminar, desactiva todos menos buscar
    elif modo in ("consultar", "eliminar"):
        guardar_estado = "disabled"
        descargar_estado = "disabled"
        # Puedes decidir si buscar está activo o no en estos modos

    btn_guardar.configure(state=guardar_estado)
    btn_descargar.configure(state=descargar_estado)
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