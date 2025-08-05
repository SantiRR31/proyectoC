import tkinter as tk
from tkinter import filedialog as fd
import customtkinter as ctk
from widgets.widgets import *
from styles.styles import *
import json
from PIL import Image
import os
from utils.config_utils import cargar_config, actualizar_config
from utils.rutas import ruta_absoluta
from utils.config_utils import cargar_config
CONFIG_PATH = "config.json"



def mostrar_ajustes(frame_contenido):
    for widget in frame_contenido.winfo_children():
        widget.destroy()
        
    config = cargar_config()
    carpeta_destino = tk.StringVar(value=config.get("carpeta_destino"))
    clave_cecati = tk.StringVar(value=config.get("clave_cecati"))
    banco_caja = tk.StringVar(value=config.get("banco_caja",))
    no_cecati = tk.StringVar(value=config.get("no_cecati",))
    no_cuenta = tk.StringVar(value=config.get("no_cuenta"))
    cuenta_cheques = tk.StringVar(value=config.get("cuenta_cheques"))
    estado = tk.StringVar(value=config.get("estado"))
    firmas = config.get("firmas", {})
    elaboro = tk.StringVar(value=firmas.get("elaboro", ""))
    reviso = tk.StringVar(value=firmas.get("reviso", ""))
    autorizo = tk.StringVar(value=firmas.get("autorizo", ""))
    director = tk.StringVar(value=firmas.get("director", ""))

    

    def selecionar_carpeta():
        carpeta = fd.askdirectory(title="Seleccionar carpeta de destino")
        if carpeta:
            carpeta_destino.set(carpeta)
            actualizar_config("carpeta_destino", carpeta)

    def actualizar_clave_cecati(nueva_clave):
        clave_cecati.set(nueva_clave)
        actualizar_config("clave_cecati", nueva_clave)
                
    def actualizar_banco_caja(nuevo_banco):
        banco_caja.set(nuevo_banco)
        actualizar_config("banco_caja", nuevo_banco)
    
    def actualizar_noCecati(nuevo_no):
        no_cecati.set(nuevo_no)
        actualizar_config("no_cecati",nuevo_no)
        
    def actualizar_noCuenta(nuevo_no):
        no_cuenta.set(nuevo_no)
        actualizar_config("no_cuenta", nuevo_no)
        
    def actualizar_cuentaCheques(nueva_cta):
        cuenta_cheques.set(nueva_cta)
        actualizar_config("cuenta_cheques",nueva_cta)
        
    def actualizar_estado(nuevo_estado):
        estado.set(nuevo_estado)
        actualizar_config("estado", nuevo_estado)
        
    def actualizar_elaboro(nuevo_valor):
        elaboro.set(nuevo_valor)
        actualizar_config("firmas.elaboro", nuevo_valor)

    def actualizar_reviso(nuevo_valor):
        reviso.set(nuevo_valor)
        actualizar_config("firmas.reviso", nuevo_valor)

    def actualizar_autorizo(nuevo_valor):
        autorizo.set(nuevo_valor)
        actualizar_config("firmas.autorizo", nuevo_valor)

    def actualizar_director(nuevo_valor):
        director.set(nuevo_valor)
        actualizar_config("firmas.director", nuevo_valor)



    # Título principal
    ctk.CTkLabel(
        frame_contenido,
        text="Ajustes",
        font=FUENTE_FORMULARIO_T,
        text_color="#d31329"  
    ).pack(pady=(20, 10))

    # Card principal
    contenedor_principal = ctk.CTkScrollableFrame(
        frame_contenido, 
        fg_color="transparent"
    )
    contenedor_principal.pack(fill="both", expand=True, padx=30, pady=20)

    # Sección de datos institucionales
    seccion_datos = ctk.CTkFrame(contenedor_principal, fg_color=("#faf7f6", "#191919"), corner_radius=12)
    seccion_datos.pack(fill="x", padx=30, pady=(30, 15))

    ctk.CTkLabel(
        seccion_datos,
        text="Datos institucionales",
        font=FUENTE_SUBMENU,
        text_color="#d31329"
    ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(10, 5))
    
    
    def crear_fila_ajuste(parent, row, label, variable, abrir_ventana_callback):
        ctk.CTkLabel(
            parent, 
            text=label, 
            font=FUENTE_LABEL
        ).grid(row=row, column=0, padx=10, pady=10, sticky="w")
        
        ctk.CTkEntry(
            parent, 
            textvariable=variable, 
            state="readonly", 
            width=180
        ).grid(row=row, column=1, padx=10, pady=10, sticky="we")
        
        ctk.CTkButton(
            parent,
            text="Cambiar",
            width=90,
            corner_radius=8,
            command=abrir_ventana_callback,
            fg_color="#d10d2f",
            hover_color="#d93954",
    ).grid(row=row, column=2, padx=10, pady=10)
        
    crear_fila_ajuste(
        seccion_datos, 1, "Estado:", estado,
        lambda: abrir_ventana_edicion(frame_contenido, "Cambiar Estado", "Estado actual:", estado, "Nuevo estado:", actualizar_estado)
    )

    crear_fila_ajuste(
        seccion_datos, 2, "Clave CECATI:", clave_cecati,
        lambda: abrir_ventana_edicion(frame_contenido, "Cambiar Clave CECATI", "Clave actual:", clave_cecati, "Nueva clave:", actualizar_clave_cecati, maxlen=10)
    )

    crear_fila_ajuste(
        seccion_datos, 3, "Banco/Caja:", banco_caja,
        lambda: abrir_ventana_edicion(frame_contenido, "Cambiar Banco o Caja", "Banco actual:", banco_caja, "Nuevo banco:", actualizar_banco_caja)
    )

    crear_fila_ajuste(
        seccion_datos, 4, "No cecati:", no_cecati,
        lambda: abrir_ventana_edicion(frame_contenido, "Cambiar No Cecati", "No actual:", no_cecati, "Nuevo No:", actualizar_noCecati, maxlen=10)
    )
    
    crear_fila_ajuste (
        seccion_datos, 5 , "Numero de Cuenta:", no_cuenta,
        lambda: abrir_ventana_edicion(frame_contenido,"Cambiar Numero de cuenta", "Numero de cuenta actual:", no_cuenta, "Nuevo numero de cuenta:", actualizar_noCuenta, maxlen= 10)
    )
    
    crear_fila_ajuste(
        seccion_datos, 6, "Cuenta de cheques:", cuenta_cheques,
        lambda: abrir_ventana_edicion(frame_contenido, "Cambiar Cuenta de cheques", "Cuenta actual:", cuenta_cheques, "Nueva cuenta:", actualizar_cuentaCheques, maxlen=10)
    )
    seccion_datos.grid_columnconfigure(1, weight=1)
    
    # Separador visual
    ctk.CTkFrame(contenedor_principal, height=2, fg_color=("#191919","#faf7f6")).pack(fill="x", padx=30, pady=10)
    
    
    seccion_firmas = ctk.CTkFrame(contenedor_principal, fg_color= ("#faf7f6", "#191919") , corner_radius=12)
    seccion_firmas.pack(fill="x", padx=30, pady=(0, 15))
    
    ctk.CTkLabel(
        seccion_firmas,
        text= "Firmas responsables (Elaboró, Revisó, Autorizó)",
        font=FUENTE_SUBMENU,
        text_color="#d31329", 
    ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(10, 5))
    
    crear_fila_ajuste(
    seccion_firmas, 1, "Elaboró:", elaboro,
    lambda: abrir_ventana_edicion(frame_contenido, "Editar nombre", "Nombre actual:", elaboro, "Nuevo nombre:", actualizar_elaboro)
)

    crear_fila_ajuste(
        seccion_firmas, 2, "Revisó:", reviso,
        lambda: abrir_ventana_edicion(frame_contenido, "Editar nombre", "Nombre actual:", reviso, "Nuevo nombre:", actualizar_reviso)
    )

    crear_fila_ajuste(
        seccion_firmas, 3, "Autorizó:", autorizo,
        lambda: abrir_ventana_edicion(frame_contenido, "Editar nombre", "Nombre actual:", autorizo, "Nuevo nombre:", actualizar_autorizo)
    )
    crear_fila_ajuste(
        seccion_firmas, 4, "Director:", director,
        lambda: abrir_ventana_edicion(frame_contenido, "Editar nombre", "Nombre actual:", director, "Nuevo nombre:", actualizar_director)
    )

    seccion_firmas.grid_columnconfigure(1, weight=1)
    

    # Sección de carpeta de destino
    seccion_carpeta = ctk.CTkFrame(contenedor_principal, fg_color= ("#faf7f6", "#191919") , corner_radius=12)
    seccion_carpeta.pack(fill="x", padx=30, pady=(0, 15))

    ctk.CTkLabel(
        seccion_carpeta,
        text="Carpeta de destino para archivos",
        font=FUENTE_SUBMENU,
        text_color="#d31329", 
    ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(10, 5))

    ctk.CTkLabel(seccion_carpeta, text="Ruta:", font=FUENTE_LABEL).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ctk.CTkEntry(seccion_carpeta, textvariable=carpeta_destino, state="readonly", width=300).grid(row=1, column=1, padx=10, pady=10, sticky="we")
    ctk.CTkButton(
        seccion_carpeta,
        text="Seleccionar",
        width=90,
        corner_radius=8,
        fg_color="#d10d2f",
        hover_color="#d93954",
        command=selecionar_carpeta
    ).grid(row=1, column=2, padx=10, pady=10)

    seccion_carpeta.grid_columnconfigure(1, weight=1)

    # Botón de ayuda y créditos
    ctk.CTkFrame(contenedor_principal, height=2, fg_color="#CAC4D0").pack(fill="x", padx=30, pady=10)
    btn_ayuda = ctk.CTkButton(
        contenedor_principal,
        text="¿Ayuda?",
        corner_radius=8,
        command=abrir_ventana_soporte,
        fg_color="#d10d2f",
        hover_color="#d93954",
        image = ctk.CTkImage(Image.open(ruta_absoluta("assets/help.png")), size=(18, 18))
    )
    btn_ayuda.pack(pady=(10, 0))

    ctk.CTkLabel(
        contenedor_principal,
        text="Desarrollado por Ariel y Santiago - UTSJR © 2025\n Para que los cambios surtan efecto, reinicia la aplicación.",
        font=("Arial", 12),
        text_color="#888"
    ).pack(side="bottom", pady=10)

# Cambia las ventanas de cambio de clave y banco para que llamen a las funciones de actualización:
def abrir_ventana_clave(frame_contenido, clave_cecati, actualizar_callback):
    ventana = ctk.CTkToplevel(frame_contenido)
    ventana.title("Cambiar Clave CECATI")
    ventana.geometry("400x250")
    ventana.resizable(False, False)

    ventana.grab_set()
    ventana.focus_force()

    ctk.CTkLabel(ventana, text="Clave actual:", font=FUENTE_LABEL).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
    ctk.CTkEntry(ventana, state="readonly", textvariable=clave_cecati).grid(row=1, column=0, padx=20, pady=5, sticky="we")

    ctk.CTkLabel(ventana, text="Nueva clave:", font=FUENTE_LABEL).grid(row=2, column=0, padx=20, pady=(15, 5), sticky="w")
    nueva_clave_var = tk.StringVar()
    
    def limitar_y_mayusculas(*args):
        valor = nueva_clave_var.get().upper()
        if len(valor) > 10:
            valor = valor[:10]
        nueva_clave_var.set(valor)

    nueva_clave_var.trace_add("write", limitar_y_mayusculas)

    entry_nueva = ctk.CTkEntry(ventana, textvariable=nueva_clave_var)
    entry_nueva.grid(row=3, column=0, padx=20, pady=5, sticky="we")
    entry_nueva.focus_set()

    def guardar_clave():
        nueva_clave = nueva_clave_var.get().strip()
        if nueva_clave:
            actualizar_callback(nueva_clave)
            ventana.destroy()

    frame_botones = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_botones.grid(row=4, column=0, pady=20)

    btn_guardar = ctk.CTkButton(frame_botones, text="Guardar", fg_color="#008d62", hover_color="#2ca880", command=guardar_clave)
    btn_guardar.pack(side="left", padx=10)

    btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", text_color="black", fg_color="#ffb201", hover_color="#ffd300", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=10)

    ventana.grid_columnconfigure(0, weight=1)

def abrir_ventana_banco(frame_contenido, banco_caja, actualizar_callback):
    ventana = ctk.CTkToplevel(frame_contenido)
    ventana.title("Cambiar Banco o Caja")
    ventana.geometry("400x250")
    ventana.resizable(False, False)

    ventana.grab_set()
    ventana.focus_force()

    ctk.CTkLabel(ventana, text="Banco actual:", font=FUENTE_LABEL).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
    ctk.CTkEntry(ventana, state="readonly", textvariable=banco_caja).grid(row=1, column=0, padx=20, pady=5, sticky="we")

    ctk.CTkLabel(ventana, text="Nuevo banco:", font=FUENTE_LABEL).grid(row=2, column=0, padx=20, pady=(15, 5), sticky="w")
    nuevo_banco_var = tk.StringVar()
    
    def limitar_y_mayusculas(*args):
        valor = nuevo_banco_var.get().upper()
        nuevo_banco_var.set(valor)

    nuevo_banco_var.trace_add("write", limitar_y_mayusculas)

    entry_nueva = ctk.CTkEntry(ventana, textvariable=nuevo_banco_var)
    entry_nueva.grid(row=3, column=0, padx=20, pady=5, sticky="we")
    entry_nueva.focus_set()

    def guardar_banco():
        nuevo_banco = nuevo_banco_var.get().strip()
        if nuevo_banco:
            actualizar_callback(nuevo_banco)
            ventana.destroy()

    frame_botones = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_botones.grid(row=4, column=0, pady=20)

    btn_guardar = ctk.CTkButton(frame_botones, text="Guardar", fg_color="#008d62", hover_color="#2ca880", command=guardar_banco)
    btn_guardar.pack(side="left", padx=10)

    btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar",text_color="black", fg_color="#ffb201", hover_color="#ffd300", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=10)

    ventana.grid_columnconfigure(0, weight=1)
    
def abrir_ventana_soporte():
    ventana = ctk.CTkToplevel()
    ventana.title("Soporte de la aplicación")
    ventana.geometry("400x300")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.focus_force()

    ctk.CTkLabel(
        ventana,
        text="¿Tienes dudas o necesitas ayuda?",
        font=("Arial", 16, "bold")
    ).pack(pady=(20, 10))

    ctk.CTkLabel(
        ventana,
        text="Puedes contactar al equipo de soporte\npor medio del siguiente correo electrónico:",
        font=("Arial", 12),
        justify="center"
    ).pack(pady=(0, 10))

    correo1 = "santiagorr.ti23@utsjr.edu.mx"
    correo2 = "arields.ti23@utsjr.edu.mx"

    # Campo para correo 1
    entry_correo = ctk.CTkEntry(ventana, width=300)
    entry_correo.insert(0, correo1)
    entry_correo.configure(state="readonly")
    entry_correo.pack(pady=(10, 5))

    # Botón para copiar correo 1
    btn_copiar1 = ctk.CTkButton(
        ventana,
        text="Copiar correo 1",
        fg_color="#d10d2f",
        hover_color="#d93954",
        command=lambda: copiar_al_portapapeles(correo1)
    )
    btn_copiar1.pack(pady=(0, 10))

    # Campo para correo 2
    entry_correo2 = ctk.CTkEntry(ventana, width=300)
    entry_correo2.insert(0, correo2)
    entry_correo2.configure(state="readonly")
    entry_correo2.pack(pady=(10, 5))

    # Botón para copiar correo 2
    btn_copiar2 = ctk.CTkButton(
        ventana,
        text="Copiar correo 2",
        fg_color="#d10d2f",
        hover_color="#d93954",
        command=lambda: copiar_al_portapapeles(correo2)
    )
    btn_copiar2.pack(pady=(0, 10))

    # Función para copiar al portapapeles
    def copiar_al_portapapeles(correo):
        ventana.clipboard_clear()
        ventana.clipboard_append(correo)
        ventana.update()

    btn_cerrar = ctk.CTkButton(ventana, text="Cerrar", fg_color="#d10d2f", hover_color="#d93954", command=ventana.destroy)
    btn_cerrar.pack(pady=(0, 10))
    btn_cerrar = ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy)
    btn_cerrar.pack(pady=(0, 10))
    
def abrir_ventana_edicion(frame_contenido, titulo, label_actual, variable_actual, label_nuevo, actualizar_callback, maxlen=100):
    ventana = ctk.CTkToplevel(frame_contenido)
    ventana.title(titulo)
    ventana.geometry("400x300")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.focus_force()

    ctk.CTkLabel(ventana, text=label_actual, font=FUENTE_LABEL).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
    ctk.CTkEntry(ventana, state="readonly", textvariable=variable_actual).grid(row=1, column=0, padx=20, pady=5, sticky="we")

    ctk.CTkLabel(ventana, text=label_nuevo, font=FUENTE_LABEL).grid(row=2, column=0, padx=20, pady=(15, 5), sticky="w")
    nuevo_valor_var = tk.StringVar()

    def limitar_y_mayusculas(*args):
        valor = nuevo_valor_var.get().upper()
        if len(valor) > maxlen:
            valor = valor[:maxlen]
        nuevo_valor_var.set(valor)

    nuevo_valor_var.trace_add("write", limitar_y_mayusculas)

    entry_nueva = ctk.CTkEntry(ventana, textvariable=nuevo_valor_var)
    entry_nueva.grid(row=3, column=0, padx=20, pady=5, sticky="we")
    entry_nueva.focus_set()

    def guardar():
        nuevo_valor = nuevo_valor_var.get().strip()
        if nuevo_valor:
            actualizar_callback(nuevo_valor)
            ventana.destroy()
            
    ctk.CTkLabel(
        ventana,
        text="* Por favor, reinicie la aplicación para que los cambios \ntengan efecto.",
        font=FUENTE_LABEL,
        text_color="#FFA500"  # Puedes cambiar el color según tu estilo
    ).grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")


    frame_botones = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_botones.grid(row=5, column=0, pady=20)

    ctk.CTkButton(frame_botones, text="Guardar", command=guardar, fg_color="#d10d2f", hover_color="#d93954").pack(side="left", padx=10)
    ctk.CTkButton(frame_botones, text="Cancelar", command=ventana.destroy, fg_color="#d10d2f", hover_color="#d93954").pack(side="left", padx=10)

    ventana.grid_columnconfigure(0, weight=1)
