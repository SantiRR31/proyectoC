import tkinter as tk
import customtkinter as ctk
import sqlite3
import datetime
from PIL import Image
from customtkinter import CTkImage

def obtener_fecha_actual():
    """Devuelve la fecha actual en formato 'DD-MM-AAAA'."""
    return datetime.datetime.now().strftime("%d-%m-%Y")

def mostrar_formulario_ingresos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()

    titulo = ctk.CTkLabel(frame_padre, text="Póliza de Ingresos", font=("Arial", 28, "bold"))
    titulo.pack(pady=30)

    # --- CONTENEDOR PRINCIPAL (Scroll + Botones fijos) ---
    contenedor_principal = ctk.CTkFrame(frame_padre, fg_color="transparent")
    contenedor_principal.pack(fill="both", expand=True)

    # --- CONTENIDO CON SCROLL ---
    contenedor_general = ctk.CTkScrollableFrame(contenedor_principal, fg_color="transparent", corner_radius=15)
    contenedor_general.pack(fill="both", expand=True, padx=30, pady=(10, 0))  # sin padding abajo

    for i in range(3):
        contenedor_general.grid_columnconfigure(i, weight=1)

    # --- SECCIÓN DATOS PÓLIZA ---
    seccion_poliza = ctk.CTkFrame(contenedor_general, fg_color="transparent")
    seccion_poliza.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 20))

    label_poliza = ctk.CTkLabel(seccion_poliza, text="Datos de la Póliza", font=("Arial", 20, "bold"))
    label_poliza.pack(anchor="w", pady=10)

    entrada_frame = ctk.CTkFrame(seccion_poliza, fg_color="transparent")
    entrada_frame.pack(fill="x")
    
    # Configuración de columnas para labels + entries
    entrada_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
    
    # Fila 1 - Fecha y Número de Póliza
    lbl_fecha = ctk.CTkLabel(entrada_frame, text="Fecha:", font=("Arial", 14))
    lbl_fecha.grid(row=0, column=0, padx=(10,5), pady=5, sticky="w")
    fecha_policia = ctk.CTkEntry(entrada_frame, placeholder_text="📅 Fecha de ingreso")
    fecha_policia.grid(row=0, column=1, padx=(5,10), pady=5, sticky="ew")
    fecha_policia.insert(0, obtener_fecha_actual())
    fecha_policia.configure(state="readonly")
    
    lbl_no_poliza = ctk.CTkLabel(entrada_frame, text="No. Póliza:", font=("Arial", 14))
    lbl_no_poliza.grid(row=0, column=2, padx=(10,5), pady=5, sticky="w")
    no_poliza = ctk.CTkEntry(entrada_frame, placeholder_text="🔢 No. Póliza")
    no_poliza.grid(row=0, column=3, padx=(5,10), pady=5, sticky="ew")

    # Fila 2 - Banco y Fecha Depósito
    lbl_banco = ctk.CTkLabel(entrada_frame, text="Banco/Caja:", font=("Arial", 14))
    lbl_banco.grid(row=1, column=0, padx=(10,5), pady=5, sticky="w")
    banco_o_caja = ctk.CTkEntry(entrada_frame, placeholder_text="🏦 Banco o Caja")
    banco_o_caja.grid(row=1, column=1, padx=(5,10), pady=5, sticky="ew")

    lbl_fecha_deposito = ctk.CTkLabel(entrada_frame, text="Fecha Depósito:", font=("Arial", 14))
    lbl_fecha_deposito.grid(row=1, column=2, padx=(10,5), pady=5, sticky="w")
    fecha_deposito = ctk.CTkEntry(entrada_frame, placeholder_text="📅 Fecha del Depósito")
    fecha_deposito.grid(row=1, column=3, padx=(5,10), pady=5, sticky="ew")

    # Fila 3 - Importe
    lbl_cuanto_pago = ctk.CTkLabel(entrada_frame, text="Importe:", font=("Arial", 14))
    lbl_cuanto_pago.grid(row=2, column=0, padx=(10,5), pady=5, sticky="w")
    cuanto_pago = ctk.CTkEntry(entrada_frame, placeholder_text="💰 Importe")
    cuanto_pago.grid(row=2, column=1, columnspan=3, padx=(5,10), pady=5, sticky="ew")

    entrada_frame.grid_columnconfigure((0, 1), weight=1)

    # --- SECCIÓN FILAS ADICIONALES ---
    seccion_filas = ctk.CTkFrame(contenedor_general, fg_color="transparent")
    seccion_filas.grid(row=2, column=0, columnspan=3, sticky="ew")

    label_filas = ctk.CTkLabel(seccion_filas, text="Clave", font=("Arial", 20, "bold"))
    label_filas.pack(anchor="w", pady=10)

    frame_filas = ctk.CTkFrame(seccion_filas, fg_color="transparent")
    frame_filas.pack(fill="x")

    entradas = []

    def buscar_denominacion_db(clave):
        conn = sqlite3.connect('prueba.db')
        cursor = conn.cursor()
        cursor.execute("SELECT denominacion FROM partidasIngresos WHERE partida = ?", (clave,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else "No encontrada"

    def llenar_denominacion(event, entrada_clave, entrada_resultado):
        clave = entrada_clave.get()
        denominacion = buscar_denominacion_db(clave)
        entrada_resultado.configure(state="normal")
        entrada_resultado.delete(0, tk.END)
        entrada_resultado.insert(0, denominacion)
        entrada_resultado.configure(state="readonly")

    def agregar_fila(enfocar_nueva_clave=False):
        fila_frame = ctk.CTkFrame(frame_filas, fg_color="transparent")
        fila_frame.pack(fill="x", pady=5)

        entrada_clave = ctk.CTkEntry(fila_frame, placeholder_text="🔑 Clave")
        entrada_clave.grid(row=0, column=0, padx=10, sticky="ew")

        entrada_resultado = ctk.CTkEntry(fila_frame, placeholder_text="Denominación", state="disabled")
        entrada_resultado.grid(row=0, column=1, padx=10, sticky="ew")

        entrada_abono = ctk.CTkEntry(fila_frame, placeholder_text="Abono")
        entrada_abono.grid(row=0, column=2, padx=10, sticky="ew")

        entrada_clave.bind("<FocusOut>", lambda event: llenar_denominacion(event, entrada_clave, entrada_resultado))
        entrada_clave.bind("<Return>", lambda event: entrada_abono.focus_set())
        entrada_abono.bind("<Return>", lambda event: agregar_fila(enfocar_nueva_clave=True))

        btn_eliminar = ctk.CTkButton(fila_frame, text="❌", width=30, fg_color="#d10d2f", hover_color="#d93954", corner_radius=5,
                                     command=lambda: fila_frame.destroy())
        btn_eliminar.grid(row=0, column=3, padx=5)

        fila_frame.grid_columnconfigure((0, 1, 2), weight=1)
        entradas.append((entrada_clave, entrada_resultado, entrada_abono))

        if enfocar_nueva_clave:
            entrada_clave.focus_set()

    agregar_fila()

    btn_agregar_fila = ctk.CTkButton(seccion_filas, text="➕ Agregar", command=agregar_fila, corner_radius=32,
                                     fg_color="#008d62", hover_color="#2ca880")
    btn_agregar_fila.pack(pady=10)

    # --- BOTONES FINALES FIJOS ABAJO ---
    botones_frame = ctk.CTkFrame(contenedor_principal, fg_color="transparent")
    botones_frame.pack(fill="x", pady=10, padx=20, anchor="e")

    imgBtnGuardar = Image.open("assets/check.png")
    btn_guardar = ctk.CTkButton(
        botones_frame, 
        text="Guardar", 
        width=120, 
        fg_color="#004b8f", 
        hover_color="#0065a5", 
        corner_radius=32,
        image=CTkImage(imgBtnGuardar, size=(20, 20))  # nota: es "image", no "Image"
    )
    btn_guardar.pack(side="right", padx=10)

    imgBtnDescargar = Image.open("assets/downlo.png")
    btn_descargar = ctk.CTkButton(
        botones_frame,
        text="Descargar",
        width=120,
        fg_color="#008d62",
        hover_color="#2ca880",
        corner_radius=32,
        image=CTkImage(imgBtnDescargar, size=(20, 20))  # nota: es "image", no "Image"
    )
    btn_descargar.pack(side="right", padx=10)
