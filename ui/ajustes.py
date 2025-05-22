import tkinter as tk
import customtkinter as ctk
from widgets.widgets import *
from styles.styles import *


def mostrar_ajustes(frame_padre, clave_cecati):
    for widget in frame_padre.winfo_children():
        widget.destroy()

    # Título
    ctk.CTkLabel(frame_padre, text="Ajustes", font=FUENTE_FORMULARIO_T).pack(pady=(20, 10))

    # Contenedor principal
    contenedor_principal = ctk.CTkFrame(frame_padre, corner_radius=15)
    contenedor_principal.pack(fill="both", expand=True, padx=20, pady=10)

    # Sección de entrada
    seccion_items = ctk.CTkFrame(contenedor_principal, corner_radius=15)
    seccion_items.pack(fill="x", padx=20, pady=(20, 10))

    entrada_clave = ctk.CTkFrame(seccion_items, fg_color=ENTRADA_FRAME_C, corner_radius=15)
    entrada_clave.pack(fill="x", padx=10, pady=10)
    entrada_clave.grid_columnconfigure((0, 1, 2, 3), weight=1)

    # Entry de la clave del plantel
    # Etiqueta para la clave
    ctk.CTkLabel(entrada_clave, text="Clave CECATI:", font=FUENTE_LABEL).grid(
        row=0, column=0, padx=(10, 5), pady=5, sticky="w"
    )

    # Entry en modo solo lectura
    cta_cheques = ctk.CTkEntry(
        entrada_clave,
        textvariable=clave_cecati,
        width=200,
        state="readonly"
    )
    cta_cheques.grid(row=0, column=1, padx=(5, 10), pady=5, sticky="w")


    # Botón para cambiar clave
    btn_frame = ctk.CTkFrame(contenedor_principal, fg_color="transparent")
    btn_frame.pack(fill="x", pady=(0, 10), padx=20)

    btn_cambiar_clave = ctk.CTkButton(
        btn_frame,
        text="Cambiar clave",
        width=120,
        fg_color="#004b8f",
        hover_color="#0065a5",
        corner_radius=10,
        command=lambda: abrir_ventana_clave(frame_padre, clave_cecati)
    )
    btn_cambiar_clave.pack(side="right")

    # Créditos
    creditos_label = ctk.CTkLabel(
        frame_padre,
        text="Desarrollado por Ariel y Santiago - UTSJR © 2025",
        font=("Arial", 10),
        text_color="gray"
    )
    creditos_label.pack(side="bottom", pady=10)
    
    btn_soporte = ctk.CTkButton(frame_padre, text="¿Ayuda?", command=abrir_ventana_soporte)
    btn_soporte.pack(pady=10)


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
    
def abrir_ventana_soporte():
    ventana = ctk.CTkToplevel()
    ventana.title("Soporte de la aplicación")
    ventana.geometry("400x250")
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

    correo = "santiagorr.ti23@utsjr.edu.mx"
    entry_correo = ctk.CTkEntry(ventana, width=300)
    entry_correo.insert(0, correo)
    entry_correo.configure(state="readonly")
    entry_correo.pack(pady=10)

    def copiar_al_portapapeles():
        ventana.clipboard_clear()
        ventana.clipboard_append(correo)
        ventana.update()

    btn_copiar = ctk.CTkButton(ventana, text="Copiar correo", command=copiar_al_portapapeles)
    btn_copiar.pack(pady=(5, 10))

    btn_cerrar = ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy)
    btn_cerrar.pack(pady=(0, 10))




