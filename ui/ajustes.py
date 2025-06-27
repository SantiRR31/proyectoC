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

CONFIG_PATH = "config.json"


def cargar_config():
    # Valores por defecto
    defaults = {
        "carpeta_destino": "~/Documentos/Cecati122/Polizas",
        "clave_cecati": "22DBT0005P",
        "banco_caja": "BANORTE"
    }
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            try:
                config = json.load(f)
            except Exception:
                config = {}
    # Asegura que todas las claves existan
    for key, value in defaults.items():
        if key not in config:
            config[key] = value
    return config


def mostrar_ajustes(frame_contenido):
    for widget in frame_contenido.winfo_children():
        widget.destroy()
        
    config = cargar_config()
    carpeta_destino = tk.StringVar(value=config.get("carpeta_destino", "~/Documentos/Cecati122/Polizas"))
    clave_cecati = tk.StringVar(value=config.get("clave_cecati", "22DBT0005P"))
    banco_caja = tk.StringVar(value=config.get("banco_caja", "BANORTE"))


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

    # Título principal
    ctk.CTkLabel(
        frame_contenido,
        text="Ajustes",
        font=FUENTE_FORMULARIO_T,
        text_color="#d31329"  
    ).pack(pady=(20, 10))

    # Card principal
    contenedor_principal = ctk.CTkFrame(frame_contenido, corner_radius=18, fg_color=("#faf7f6", "#191919"))
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

    # Clave CECATI
    ctk.CTkLabel(seccion_datos, text="Clave CECATI:", font=FUENTE_LABEL).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ctk.CTkEntry(seccion_datos, textvariable=clave_cecati, state="readonly", width=180).grid(row=1, column=1, padx=10, pady=10, sticky="we")
    ctk.CTkButton(
        seccion_datos,
        text="Cambiar",
        width=90,
        corner_radius=8,
        fg_color="#d10d2f",
        hover_color="#d93954",
        command=lambda: abrir_ventana_clave(frame_contenido, clave_cecati, actualizar_clave_cecati)
    ).grid(row=1, column=2, padx=10, pady=10)

    # Banco/Caja
    ctk.CTkLabel(seccion_datos, text="Banco/Caja:", font=FUENTE_LABEL).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    ctk.CTkEntry(seccion_datos, textvariable=banco_caja, state="readonly", width=180).grid(row=2, column=1, padx=10, pady=10, sticky="we")
    ctk.CTkButton(
        seccion_datos,
        text="Cambiar",
        width=90,
        corner_radius=8,
        fg_color="#d10d2f",
        hover_color="#d93954",
        command=lambda: abrir_ventana_banco(frame_contenido, banco_caja, actualizar_banco_caja)
    ).grid(row=2, column=2, padx=10, pady=10)

    seccion_datos.grid_columnconfigure(1, weight=1)

    # Separador visual
    ctk.CTkFrame(contenedor_principal, height=2, fg_color=("#191919","#faf7f6")).pack(fill="x", padx=30, pady=10)


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
        text="Desarrollado por Ariel y Santiago - UTSJR © 2025",
        font=("Arial", 10),
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