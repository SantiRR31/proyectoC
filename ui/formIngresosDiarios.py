import tkinter as tk
import customtkinter as ctk

def mostrar_formulario_ingresos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # --- TÍTULO PRINCIPAL ---
    titulo = ctk.CTkLabel(frame_padre, text="Póliza de Ingresos", font=("Arial", 28, "bold"))
    titulo.pack(pady=30)

    # --- CONTENEDOR GENERAL ---
    contenedor_general = ctk.CTkFrame(frame_padre, fg_color="#F7F9FC", corner_radius=15)
    contenedor_general.pack(fill="both", expand=True, padx=30, pady=10)

    # Configurar columnas generales
    for i in range(3):
        contenedor_general.grid_columnconfigure(i, weight=1)

    # --- SECCIÓN 1: DATOS DE LA PÓLIZA ---
    seccion_poliza = ctk.CTkFrame(contenedor_general, fg_color="transparent")
    seccion_poliza.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 20))

    label_poliza = ctk.CTkLabel(seccion_poliza, text=" Datos de la Póliza", font=("Arial", 20, "bold"))
    label_poliza.pack(anchor="w", pady=10)

    entrada_frame = ctk.CTkFrame(seccion_poliza, fg_color="transparent")
    entrada_frame.pack(fill="x")

    fecha_policia = ctk.CTkEntry(entrada_frame, placeholder_text="📅 Fecha de ingreso")
    fecha_policia.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    no_poliza = ctk.CTkEntry(entrada_frame, placeholder_text="🔢 No. Póliza")
    no_poliza.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    banco_o_caja = ctk.CTkEntry(entrada_frame, placeholder_text="🏦 Banco o Caja")
    banco_o_caja.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    fecha_deposito = ctk.CTkEntry(entrada_frame, placeholder_text="📅 Fecha del Depósito")
    fecha_deposito.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    cuanto_pago = ctk.CTkEntry(entrada_frame, placeholder_text="💰 Cuánto Pago")
    cuanto_pago.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    # Hacer entradas responsivas
    entrada_frame.grid_columnconfigure((0, 1), weight=1)
    
    
    # --- SECCIÓN 3: FILAS ADICIONALES ---
    seccion_filas = ctk.CTkFrame(contenedor_general, fg_color="transparent")
    seccion_filas.grid(row=2, column=0, columnspan=3, sticky="ew")

    label_filas = ctk.CTkLabel(seccion_filas, text="Claves y Partidas", font=("Arial", 20, "bold"))
    label_filas.pack(anchor="w", pady=10)

    frame_filas = ctk.CTkFrame(seccion_filas, fg_color="transparent")
    frame_filas.pack(fill="x")

    def agregar_fila():
        fila_frame = ctk.CTkFrame(frame_filas, fg_color="transparent")
        fila_frame.pack(fill="x", pady=5)

        clave = ctk.CTkEntry(fila_frame, placeholder_text="🔑 Clave")
        clave.grid(row=0, column=0, padx=10, sticky="ew")

        partida = ctk.CTkEntry(fila_frame, placeholder_text="📄 Denominación")
        partida.grid(row=0, column=1, padx=10, sticky="ew")

        resultado = ctk.CTkEntry(fila_frame, placeholder_text="📊 Cargo")
        resultado.grid(row=0, column=2, padx=10, sticky="ew")

        btn_eliminar = ctk.CTkButton(
            fila_frame,
            text="❌",
            width=30,
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=lambda: fila_frame.destroy()
        )
        btn_eliminar.grid(row=0, column=3, padx=5)

    # Hacer que cada columna se expanda
        fila_frame.grid_columnconfigure((0, 1, 2), weight=1)

    agregar_fila()  # Cargar una fila por defecto

    btn_agregar_fila = ctk.CTkButton(seccion_filas, text="➕ Agregar ", command=agregar_fila, fg_color="#4CAF50", hover_color="#45A049")
    btn_agregar_fila.pack(pady=10)

    # --- BOTONES FINALES ---
    botones_frame = ctk.CTkFrame(frame_padre, fg_color="transparent")
    botones_frame.pack(pady=20)

    btn_guardar = ctk.CTkButton(botones_frame, text="💾 Guardar", width=120, fg_color="#2196F3", hover_color="#1976D2")
    btn_guardar.grid(row=0, column=0, padx=10)

    btn_descargar = ctk.CTkButton(botones_frame, text="⬇️ Descargar", width=120, fg_color="#FF9800", hover_color="#F57C00")
    btn_descargar.grid(row=0, column=1, padx=10)
