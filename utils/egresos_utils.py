from datetime import time
from datetime import datetime
from tkinter import messagebox
from styles.styles import ESTILO_LIST_SUG
from utils.utils import *
import customtkinter as ctk
import math
from db.egresosDB import *
from models.egresomodelos import *
from datetime import datetime
from utils.config_utils import cargar_config

config = cargar_config()


def formatear_numero_poliza(num_str):
        num_str = num_str.strip()
        if not num_str.isdigit():
            return num_str  # Devolver tal cual si no es número
        num = int(num_str)
        return f"{num:02d}"  # Siempre con dos dígitos, pero sin agregar 010 ni nada raro


#----------------- Funciones de captura y validación de pólizas de egresos -----------------

def capturar_poliza(form, entradas):
    try:
        poliza_id = form["poliza_id"].get() or None

        # Obtener número y sufijo desde los widgets (por ejemplo, CTkEntry)
        numero = form["numero"].get().strip()
        
        sufijo = form["sufijo"].get().strip()

        # Armar no_poliza completo
        no_poliza = f"{numero}{sufijo}" if numero and sufijo else numero

        fecha = form["fecha"].get()
        nombre = form["nombre"].get()
        monto = form["cargo"].get()
        tipo_pago = form["tipo_pago"].get()
        monto_letra = form["monto_letra"].get() or None
        clave_ref = form["clave_rastreo"].get()
        #denominacion = form["denominacion"].get() or None
        observaciones = form["observaciones"].get("1.0", "end").strip()
        no_cheque = form["no_cheque"].get() or None

        # Validaciones...
        faltantes = []
        if not no_poliza:
            faltantes.append(f"no_poliza: '{no_poliza}'")
        if not fecha:
            faltantes.append(f"fecha: '{fecha}'")
        if not nombre:
            faltantes.append(f"nombre: '{nombre}'")

        if faltantes:
            mensaje = "Faltan los siguientes campos obligatorios:\n" + "\n".join(faltantes)
            messagebox.showerror("Campos incompletos", mensaje)
            return None

        # Validación por tipo de pago...
        if tipo_pago == "CHEQUE" and not no_cheque:
            messagebox.showerror("Falta número de cheque", "Debes ingresar el número de cheque.")
            return None
        elif tipo_pago == "TRANSFERENCIA" and not clave_ref:
            messagebox.showerror("Falta clave de rastreo", "Debes ingresar la clave de rastreo.")
            return None

        # Crear objeto PolizaEgreso
        poliza = PolizaEgreso(
            poliza_id=poliza_id,
            no_poliza=no_poliza,
            fecha=fecha,
            monto=monto,
            monto_letra=monto_letra,
            nombre=nombre,
            tipo_pago=tipo_pago,
            clave_ref=clave_ref,
            #denominacion=denominacion,
            observaciones=observaciones,
            no_cheque=no_cheque
        )

        # Procesar conceptos
        total_conceptos = 0.0
        for entrada_clave, entrada_desc, entrada_importe in entradas:
            try:
                clave = entrada_clave.get().strip()
                descripcion = entrada_desc.get()
                cargo = float(entrada_importe.get())
                partida_especifica = obtener_partida_especifica_por_clave(int(clave))

                if clave and descripcion and cargo:
                    concepto = ConceptoEgreso(clave, descripcion, partida_especifica, cargo)
                    poliza.agregar_concepto(concepto)
                    total_conceptos += cargo
            except Exception as e:
                print(f"Error procesando concepto: {e}")
                continue

        # Validar que el monto general coincida con el total de conceptos
        try:
            monto_float = float(monto)
        except ValueError:
            messagebox.showerror("Error", "El monto general no es válido.")
            return None

        if abs(monto_float - total_conceptos) > 0.01:
            messagebox.showerror(
                "Totales no coinciden",
                f"El monto total de los conceptos ({total_conceptos:.2f}) no coincide con el monto general ({monto_float:.2f})."
            )
            return None

        return poliza

    except Exception as e:
        print("Error al capturar la póliza:", e)
        messagebox.showerror("Error", f"Ocurrió un error al capturar la póliza:\n{e}")
        return None





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
        #"denominacion": form["denominacion"].get(),
        "observaciones": form["observaciones"].get(),
    }
        
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

def ejecutar_con_loading(funcion, btn_guardar, btn_descargar, contenedor_principal, limpiar_formulario, es_edicion=False,*args):
    if btn_guardar is not None and btn_guardar.winfo_exists():
        btn_guardar.configure(state="disabled", text="Guardando...")

    if btn_descargar is not None and btn_descargar.winfo_exists():
        btn_descargar.configure(state="disabled", text="Descargando...")
    # Mostrar animación visual
    anim = AnimacionDescarga(contenedor_principal)
    anim.grab_set()  # Hace modal la ventana de animación
    def ejecutar():
        try:
            resultado = funcion(*args)
            if resultado:
                messagebox.showinfo("Éxito", "Poliza Guardada correctamente")
            if not es_edicion:
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
    # Si no hay contenedor principal, ejecuta sin animación y sin after
    if contenedor_principal is None:
        try:
            funcion(*args, **kwargs)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")
        return

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
    # Mapea los meses abreviados sin punto
    meses_abreviados = [
        "ene", "feb", "mar", "abr", "may", "jun",
        "jul", "ago", "sep", "oct", "nov", "dic"
    ]

    # Detecta y convierte si la fecha viene en formato 'DD/MM/YYYY'
    if "/" in fecha:
        dt = datetime.strptime(fecha, "%d/%m/%Y")
    else:
        dt = datetime.strptime(fecha, "%Y-%m-%d")

    consecutivo = obtener_siguiente_no_poliza_mes(dt.strftime("%d/%m/%Y"))
    mes = meses_abreviados[dt.month - 1]
    anio = dt.strftime("%Y")
    return f"{consecutivo}/{mes}/{anio}"




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
                entrada_desc.configure(state="normal")
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
        
def campos_obligatorios_vacios(campos, conceptos):
    # Valida los campos fijos
    if any(campo.get().strip() == "" for campo in campos):
        return True
    # Valida los conceptos (clave, descripción, importe)
    for entrada_clave, entrada_desc, entrada_importe in conceptos:
        if not entrada_clave.get().strip() or not entrada_desc.get().strip() or not entrada_importe.get().strip():
            return True
    return False


def seleccionar_sugerencia(event, entrada_clave, entrada_desc, lista_sugerencias, entradas):
    seleccion = lista_sugerencias.curselection()
    try:
        if not seleccion:
            return
        idx = seleccion[0]
        seleccionado = lista_sugerencias.coins[idx]
        entrada_clave.delete(0, tk.END)
        entrada_clave.insert(0, seleccionado["partida"])

        entrada_desc.configure(state="normal")
        entrada_desc.delete(0, tk.END)
        entrada_desc.insert(0, seleccionado["desc_partida"])
        entrada_desc.configure(state="readonly")

        # Enfocar siguiente campo
        for entrada in entradas:
            if entrada[1] == entrada_desc:
                entrada[2].focus_set()
                break
    except Exception as e:
        print(f"Error al seleccionar sugerencia: {e}")


def configurar_lista_sugerencias(
    entrada_desc, entrada_clave, conceptos_frame, entradas,
    mostrar_sugerencias, ESTILO_LIST_SUG
):
    lista_sugerencias = tk.Listbox(conceptos_frame, **ESTILO_LIST_SUG)
    
    lista_sugerencias.bind("<Double-Button-1>", 
        lambda e: seleccionar_sugerencia(e, entrada_clave, entrada_desc, lista_sugerencias, entradas))
    lista_sugerencias.bind("<Return>", 
        lambda e: seleccionar_sugerencia(e, entrada_clave, entrada_desc, lista_sugerencias, entradas))

    search_timer = None
    def throttled_search(event):
        nonlocal search_timer
        if search_timer:
            entrada_desc.after_cancel(search_timer)
        search_timer = entrada_desc.after(300, lambda: mostrar_sugerencias(event, entrada_desc, entrada_clave, lista_sugerencias))
    
    entrada_desc.bind("<KeyRelease>", throttled_search)

    def hide_on_focus_out(event):
        def hide_delayed():
            try:
                if lista_sugerencias.winfo_exists():
                    lista_sugerencias.place_forget()
            except tk.TclError:
                pass
        entrada_desc.after(200, hide_delayed)
    
    entrada_desc.bind("<FocusOut>", hide_on_focus_out)

    def mover_seleccion(event, direccion):
        if not lista_sugerencias.winfo_ismapped():
            return

        size = lista_sugerencias.size()
        if size == 0:
            return

        seleccion = lista_sugerencias.curselection()
        idx = seleccion[0] if seleccion else -1

        nuevo_idx = min(idx + 1, size - 1) if direccion == "abajo" else max(idx - 1, 0)
        
        lista_sugerencias.selection_clear(0, tk.END)
        lista_sugerencias.selection_set(nuevo_idx)
        lista_sugerencias.activate(nuevo_idx)
        lista_sugerencias.see(nuevo_idx)
        return "break"

    entrada_desc.bind("<Down>", lambda e: mover_seleccion(e, "abajo"))
    entrada_desc.bind("<Up>", lambda e: mover_seleccion(e, "arriba")) 
    
    return lista_sugerencias