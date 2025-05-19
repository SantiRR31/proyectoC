import tkinter as tk
import customtkinter as ctk
import sqlite3
from PIL import Image
from functions.funcions import obtener_fecha_actual
from db.egresosDB import buscar_denominacion_db
from customtkinter import CTkImage
from styles.styles import (
    FUENTE_FORMULARIO_T,
    FUENTE_FORMULARIO_S,
    FONDO_CONTENEDORES,
    ENTRADA_FRAME_C,
)

def mostrar_formulario_egresos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()

    # Título principal
    titulo = ctk.CTkLabel(frame_padre, text="Póliza de Egresos",font=FUENTE_FORMULARIO_T)
    titulo.pack(pady=30)

    # Contenedor principal
    contenedor_principal = ctk.CTkFrame(frame_padre, corner_radius=15)
    contenedor_principal.pack(fill="both", expand=True)

    # Scroll dentro del contenedor
    contenedor_general = ctk.CTkScrollableFrame(contenedor_principal,corner_radius=15)
    contenedor_general.pack(fill="both", expand=True, padx=30, pady=(10, 0))

    for i in range(3):
        contenedor_general.grid_columnconfigure(i, weight=1)

    # Sección datos de la póliza
    seccion_poliza = ctk.CTkFrame(contenedor_general, corner_radius=15)
    seccion_poliza.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 20))

    ctk.CTkLabel(seccion_poliza, text="Datos del cheque", font=("Arial", 20, "bold")).pack(anchor="w", pady=10)

    entrada_frame = ctk.CTkFrame(seccion_poliza, fg_color="transparent",corner_radius=15)
    entrada_frame.pack(fill="x")
    entrada_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    # Fila 1 - Fecha y número de póliza
    """ ctk.CTkLabel(entrada_frame, text="Fecha:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")
    fecha_poliza = ctk.CTkEntry(entrada_frame, placeholder_text="📅 Fecha de ingreso")
    fecha_poliza.grid(row=0, column=1, padx=(5, 10), pady=5, sticky="ew")
    fecha_poliza.insert(0, obtener_fecha_actual())
    fecha_poliza.configure(state="readonly")"""

    # No. Póliza
    ctk.CTkLabel(entrada_frame, text="No. Póliza:", font=("Arial", 14)).grid(
        row=0, column=2, padx=(10, 5), pady=5, sticky="w")
    no_poliza = ctk.CTkEntry(entrada_frame, placeholder_text="🔢 No. Póliza")
    no_poliza.grid(row=0, column=3, padx=(5, 10), pady=5, sticky="ew")

# DATOS DEL CHEQUE
    ctk.CTkLabel(entrada_frame, text="DATOS DEL CHEQUE", font=("Arial", 14, "bold")).grid(
      row=1, column=0, columnspan=4, pady=(15, 5), sticky="n")
    datos_del_cheque = ctk.CTkEntry(entrada_frame, placeholder_text="💰 DATOS DEL CHEQUE", height=40)
    datos_del_cheque.grid(row=2, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="ew")

# RECIB)
    ctk.CTkLabel(entrada_frame, text="Recibí:", font=("Arial", 14)).grid(
      row=3, column=0, columnspan=4, pady=(10, 5), sticky="n")
    recibi_entry = ctk.CTkEntry(entrada_frame, placeholder_text="💰 CH", height=40)
    recibi_entry.grid(row=4, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="ew")

    # Denominación
    lbl_denominacion = ctk.CTkLabel(entrada_frame, text="Denominación:", font=("Arial", 14))
    lbl_denominacion.grid(row=6, column=0, padx=(10, 5), pady=25, sticky="w")
    denominacion = ctk.CTkEntry(entrada_frame, placeholder_text="💵 Denominación")
    denominacion.grid(row=6, column=1, padx=(5, 10), pady=5, sticky="ew")

    # Cargo
    lbl_fecha_deposito = ctk.CTkLabel(entrada_frame, text="Cargo:", font=("Arial", 14))
    lbl_fecha_deposito.grid(row=6, column=2, padx=(10, 5), pady=5, sticky="w")
    fecha_deposito = ctk.CTkEntry(entrada_frame, placeholder_text="💰 Cargo")
    fecha_deposito.grid(row=6, column=3, padx=(5, 10), pady=5, sticky="ew")

    # Sección filas adicionales
    
    seccion_filas = ctk.CTkFrame(contenedor_general, fg_color= FONDO_CONTENEDORES, corner_radius=15)
    seccion_filas.grid(row=7, column=0, columnspan=3, sticky="ew")
    
    seccion_titulos_filas = ctk.CTkFrame(contenedor_general, corner_radius=15)
    seccion_titulos_filas.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 5))

# Column titles
    ctk.CTkLabel(seccion_titulos_filas, text="Clave", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, sticky="w")
    ctk.CTkLabel(seccion_titulos_filas, text="Denominación", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, sticky="w")
    ctk.CTkLabel(seccion_titulos_filas, text="Cargo", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=10, sticky="w")

# Asegúrate de configurar el peso de las columnas si es necesario:
    seccion_titulos_filas.grid_columnconfigure((0, 1, 2), weight=1)

    # Sección filas
    frame_filas = ctk.CTkFrame(seccion_filas, corner_radius=15)
    frame_filas.pack(fill="x")

    entradas = []
    def llenar_denominacion(event, entrada_clave, entrada_resultado):
        clave = entrada_clave.get()
        denominacion = buscar_denominacion_db(clave)
        entrada_resultado.configure(state="normal")
        entrada_resultado.delete(0, tk.END)
        entrada_resultado.insert(0, denominacion)
        entrada_resultado.configure(state="readonly")

    def actualizar_total():
        try:
            suma_total = sum(float(entrada[2].get()) for entrada in entradas if entrada[2].get().strip())
            total.configure(state="normal")
            total.delete(0, tk.END)
            total.insert(0, f"{suma_total:.2f}")
            total.configure(state="readonly")
         
            importe_valor = cuanto_pago.get().strip()
            if importe_valor:
                importe_float = float(importe_valor)
                if abs(importe_float - suma_total) < 0.01:
                    validacion_totales.configure(text="✅", text_color="#008d62")
                else:
                    validacion_totales.configure(text="❌", text_color="#d10d2f")
            else:
                validacion_totales.configure(text="❌", text_color="gray")
        except ValueError:
            pass

    def agregar_fila(enfocar_nueva_clave=False):
        fila_frame = ctk.CTkFrame(frame_filas, fg_color= FONDO_CONTENEDORES,corner_radius=15)
        fila_frame.pack(fill="x", pady=5)

        entrada_clave = ctk.CTkEntry(fila_frame, placeholder_text="🔑 Clave")
        entrada_clave.grid(row=0, column=0, padx=10, sticky="ew")

        entrada_resultado = ctk.CTkEntry(fila_frame, placeholder_text="Denominación", state="disabled")
        entrada_resultado.grid(row=0, column=1, padx=10, sticky="ew")

        entrada_abono = ctk.CTkEntry(fila_frame, placeholder_text="Cargo")
        entrada_abono.grid(row=0, column=2, padx=10, sticky="ew")
        entrada_abono.bind("<KeyRelease>", lambda event: actualizar_total())

        entrada_clave.bind("<FocusOut>", lambda event: llenar_denominacion(event, entrada_clave, entrada_resultado))
        entrada_clave.bind("<Return>", lambda event: entrada_abono.focus_set())
        entrada_abono.bind("<Return>", lambda event: agregar_fila(enfocar_nueva_clave=True))
        

        btn_eliminar = ctk.CTkButton(
            
            fila_frame,
            text="❌",
            width=30,
            fg_color="#d10d2f",
            hover_color="#d93954",
            corner_radius=5,
            command=lambda: (fila_frame.destroy(), entradas.remove((entrada_clave, entrada_resultado, entrada_abono)), actualizar_total())
        )
        btn_eliminar.grid(row=0, column=3, padx=5)

        fila_frame.grid_columnconfigure((0, 1, 2), weight=1)
        entradas.append((entrada_clave, entrada_resultado, entrada_abono))

        if enfocar_nueva_clave:
            entrada_clave.focus_set()

    agregar_fila()

    ctk.CTkButton(seccion_filas, text="➕ Agregar", command=agregar_fila, corner_radius=32,
                  fg_color="#008d62", hover_color="#2ca880").pack(pady=10)

    # Botones inferiores
    botones_frame = ctk.CTkFrame(contenedor_principal,  fg_color= FONDO_CONTENEDORES,corner_radius=15)
    botones_frame.pack(fill="x", pady=10, padx=20, anchor="e")

    ctk.CTkLabel(botones_frame, text="Total:", font=("Arial", 16)).pack(side="left", padx=(0, 10))
    total = ctk.CTkEntry(botones_frame, placeholder_text="💰 Total", state="readonly")
    total.pack(side="left", padx=(0, 10), fill="x", expand=False)

    validacion_totales = ctk.CTkLabel(botones_frame, text="❌", font=("Arial", 20))
    validacion_totales.pack(side="left", padx=(0, 10))

    imgBtnGuardar = Image.open("assets/check.png")
    ctk.CTkButton(
        botones_frame,
        text="Guardar",
        width=120,
        fg_color="#004b8f",
        hover_color="#0065a5",
        corner_radius=32,
        image=CTkImage(imgBtnGuardar, size=(20, 20))
    ).pack(side="right", padx=10)

    imgBtnDescargar = Image.open("assets/downlo.png")
    ctk.CTkButton(
        botones_frame,
        text="Descargar",
        width=120,
        fg_color="#008d62",
        hover_color="#2ca880",
        corner_radius=32,
        image=CTkImage(imgBtnDescargar, size=(20, 20))
    ).pack(side="right", padx=10)
