import tkinter as tk
import customtkinter as ctk
import sqlite3

def mostrar_formulario_ingresos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode("light")  # Modo claro
    ctk.set_default_color_theme("blue")

    titulo = ctk.CTkLabel(frame_padre, text="Póliza de Ingresos", font=("Arial", 28, "bold"))
    titulo.pack(pady=30)

    contenedor_general = ctk.CTkFrame(frame_padre, fg_color="#DBDBDB", corner_radius=15)
    contenedor_general.pack(fill="both", expand=True, padx=30, pady=10)

    for i in range(3):
        contenedor_general.grid_columnconfigure(i, weight=1)

    # --- SECCIÓN DATOS PÓLIZA ---
    seccion_poliza = ctk.CTkFrame(contenedor_general, fg_color="transparent")
    seccion_poliza.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 20))

    label_poliza = ctk.CTkLabel(seccion_poliza, text="Datos de la Póliza", font=("Arial", 20, "bold"))
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

    entrada_frame.grid_columnconfigure((0, 1), weight=1)

    # --- SECCIÓN FILAS ADICIONALES ---
    seccion_filas = ctk.CTkFrame(contenedor_general, fg_color="transparent")
    seccion_filas.grid(row=2, column=0, columnspan=3, sticky="ew")

    label_filas = ctk.CTkLabel(seccion_filas, text="Claves y Partidas", font=("Arial", 20, "bold"))
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

        entrada_resultado = ctk.CTkEntry(fila_frame, placeholder_text="📄 Denominación", state="readonly")
        entrada_resultado.grid(row=0, column=1, padx=10, sticky="ew")

        entrada_abono = ctk.CTkEntry(fila_frame, placeholder_text="📊 Abono")
        entrada_abono.grid(row=0, column=2, padx=10, sticky="ew")

        # Al salir del campo Clave, llena la denominación
        entrada_clave.bind("<FocusOut>", lambda event: llenar_denominacion(event, entrada_clave, entrada_resultado))

        # ENTER en Clave -> pasa el foco a Abono
        entrada_clave.bind("<Return>", lambda event: entrada_abono.focus_set())

        # ENTER en Abono -> agrega nueva fila y enfoca nueva Clave
        entrada_abono.bind("<Return>", lambda event: agregar_fila(enfocar_nueva_clave=True))

        # Botón para eliminar
        btn_eliminar = ctk.CTkButton(fila_frame, text="❌", width=30, fg_color="#F44336", hover_color="#D32F2F",
                                     command=lambda: fila_frame.destroy())
        btn_eliminar.grid(row=0, column=3, padx=5)

        fila_frame.grid_columnconfigure((0, 1, 2), weight=1)
        entradas.append((entrada_clave, entrada_resultado, entrada_abono))

        if enfocar_nueva_clave:
            entrada_clave.focus_set()

    agregar_fila()

    def on_enter_abono():
        agregar_fila(enfocar_nueva_clave=True)


    btn_agregar_fila = ctk.CTkButton(seccion_filas, text="➕ Agregar", command=agregar_fila,
                                     fg_color="#4CAF50", hover_color="#45A049")
    btn_agregar_fila.pack(pady=10)

    # --- BOTONES FINALES ---
    botones_frame = ctk.CTkFrame(frame_padre, fg_color="transparent")
    botones_frame.pack(pady=20)

    btn_guardar = ctk.CTkButton(botones_frame, text="💾 Guardar", width=120, fg_color="#2196F3", hover_color="#1976D2")
    btn_guardar.grid(row=0, column=0, padx=10)

    btn_descargar = ctk.CTkButton(botones_frame, text="⬇️ Descargar", width=120, fg_color="#FF9800", hover_color="#F57C00")
    btn_descargar.grid(row=0, column=1, padx=10)
