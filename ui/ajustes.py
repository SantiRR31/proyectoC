import tkinter as tk
import customtkinter as ctk
from widgets.widgets import *
from styles.styles import *


def mostrar_ajustes(frame_padre, clave_cecati, banco_caja):
    for widget in frame_padre.winfo_children():
        widget.destroy()

    # Título
    ctk.CTkLabel(
        frame_padre,
        text="Ajustes",
        font=FUENTE_FORMULARIO_T
    ).pack(pady=(20, 10))

    # Contenedor principal
    contenedor_principal = ctk.CTkFrame(frame_padre, corner_radius=15)
    contenedor_principal.pack(fill="both", expand=True, padx=20, pady=10)

    # Sección de entradas
    seccion_items = ctk.CTkFrame(contenedor_principal, corner_radius=15)
    seccion_items.pack(fill="x", padx=20, pady=(20, 10))

    for label_text, var, comando in [
        ("Clave CECATI:", clave_cecati, abrir_ventana_clave),
        ("Banco/Caja:", banco_caja, abrir_ventana_banco)
    ]:
        entrada_frame = ctk.CTkFrame(seccion_items, fg_color=ENTRADA_FRAME_C, corner_radius=15)
        entrada_frame.pack(fill="x", padx=10, pady=10)
        entrada_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Etiqueta
        ctk.CTkLabel(entrada_frame, text=label_text, font=FUENTE_LABEL).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        # Entrada de solo lectura
        ctk.CTkEntry(entrada_frame, textvariable=var, state="readonly").grid(
            row=0, column=1, padx=10, pady=10, sticky="we"
        )

        # Botón para cambiar
        ctk.CTkButton(
            entrada_frame,
            text=f"Cambiar {label_text.split(':')[0]}",
            width=120,
            fg_color="#004b8f",
            hover_color="#0065a5",
            corner_radius=10,
            command=lambda v=var, c=comando: c(frame_padre, v)
        ).grid(row=0, column=2, padx=10, pady=10)

    # Botón de ayuda centrado en la parte inferior
    ctk.CTkButton(
        frame_padre,
        text="¿Ayuda?",
        command=abrir_ventana_soporte
    ).pack(pady=(5, 0))

    # Créditos
    ctk.CTkLabel(
        frame_padre,
        text="Desarrollado por Ariel y Santiago - UTSJR © 2025",
        font=("Arial", 10),
        text_color="gray"
    ).pack(side="bottom", pady=10)


def abrir_ventana_clave(frame_padre, clave_cecati):
    ventana = ctk.CTkToplevel(frame_padre)
    ventana.title("Cambiar Clave CECATI")
    ventana.geometry("400x250")
    ventana.resizable(False, False)

    ventana.grab_set()
    ventana.focus_force()

    # Clave actual
    ctk.CTkLabel(ventana, text="Clave actual:", font=FUENTE_LABEL).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
    ctk.CTkEntry(ventana, state="readonly", textvariable=clave_cecati).grid(row=1, column=0, padx=20, pady=5, sticky="we")

    # Nueva clave
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

    # Botones
    def guardar_clave():
        nueva_clave = nueva_clave_var.get().strip()
        if nueva_clave:
            clave_cecati.set(nueva_clave)
            ventana.destroy()

    frame_botones = ctk.CTkFrame(ventana)
    frame_botones.grid(row=4, column=0, pady=20)

    btn_guardar = ctk.CTkButton(frame_botones, text="Guardar", command=guardar_clave)
    btn_guardar.pack(side="left", padx=10)

    btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=10)

    ventana.grid_columnconfigure(0, weight=1)
    
def abrir_ventana_banco(frame_padre, banco_caja):
    ventana = ctk.CTkToplevel(frame_padre)
    ventana.title("Cambiar Banco o Caja")
    ventana.geometry("400x250")
    ventana.resizable(False, False)

    ventana.grab_set()
    ventana.focus_force()

    # Clave actual
    ctk.CTkLabel(ventana, text="Banco actual:", font=FUENTE_LABEL).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
    ctk.CTkEntry(ventana, state="readonly", textvariable=banco_caja).grid(row=1, column=0, padx=20, pady=5, sticky="we")

    # Nueva clave
    ctk.CTkLabel(ventana, text="Nuevo banco:", font=FUENTE_LABEL).grid(row=2, column=0, padx=20, pady=(15, 5), sticky="w")
    nuevo_banco_var = tk.StringVar()
    
    def limitar_y_mayusculas(*args):
        valor = nuevo_banco_var.get().upper()
        nuevo_banco_var.set(valor)

    nuevo_banco_var.trace_add("write", limitar_y_mayusculas)

    
    entry_nueva = ctk.CTkEntry(ventana, textvariable=nuevo_banco_var)
    entry_nueva.grid(row=3, column=0, padx=20, pady=5, sticky="we")
    entry_nueva.focus_set()

    # Botones
    def guardar_banco():
        nuevo_banco = nuevo_banco_var.get().strip()
        if nuevo_banco:
            banco_caja.set(nuevo_banco)
            ventana.destroy()

    frame_botones = ctk.CTkFrame(ventana)
    frame_botones.grid(row=4, column=0, pady=20)

    btn_guardar = ctk.CTkButton(frame_botones, text="Guardar", command=guardar_banco)
    btn_guardar.pack(side="left", padx=10)

    btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", command=ventana.destroy)
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
        command=lambda: copiar_al_portapapeles(correo2)
    )
    btn_copiar2.pack(pady=(0, 10))

    # Función para copiar al portapapeles
    def copiar_al_portapapeles(correo):
        ventana.clipboard_clear()
        ventana.clipboard_append(correo)
        ventana.update()

    btn_cerrar = ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy)
    btn_cerrar.pack(pady=(0, 10))




