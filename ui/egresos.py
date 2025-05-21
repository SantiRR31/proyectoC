import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import xlwings as xw
from db.egresosDB import buscar_descripcion_db
from widgets.widgets import (
    crear_label,
    crear_entry,
    crear_boton,
    crear_boton_imagen
)
from utils.utils import (
    obtener_fecha_actual,
    numero_a_letras_mxn,
    abrir_carpeta,
    )


from styles.styles import (
    FUENTE_FORMULARIO_T,
    FUENTE_FORMULARIO_S,
    FONDO_CONTENEDORES,
    ENTRADA_FRAME_C,
    FUENTE_LABEL,
    FUENTE_SECCION_TITULO,
    FUENTE_VALIDACION,
    btn_eliminar_style,
    btn_agregar_style,
    btn_guardar_style,
    btn_descargar_style,
    COLOR_VALIDACION_OK,
    COLOR_VALIDACION_ERROR,
    COLOR_VALIDACION_NEUTRO,
)


def mostrar_formulario_egresos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()

    # Título principal
    ctk.CTkLabel(frame_padre, text="Póliza de Egresos", font=FUENTE_FORMULARIO_T).pack(pady=30)

    # Contenedor principal
    contenedor_principal = ctk.CTkFrame(frame_padre, corner_radius=15)
    contenedor_principal.pack(fill="both", expand=True)

    # Scroll dentro del contenedor
    contenedor_general = ctk.CTkScrollableFrame(contenedor_principal, corner_radius=15)
    contenedor_general.pack(fill="both", expand=True, padx=30, pady=(10, 0))

    for i in range(3):
        contenedor_general.grid_columnconfigure(i, weight=1)

    # Sección datos de la póliza
    seccion_poliza = ctk.CTkFrame(contenedor_general, corner_radius=15)
    seccion_poliza.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 20))

    entrada_frame = ctk.CTkFrame(seccion_poliza, fg_color=ENTRADA_FRAME_C, corner_radius=15)
    entrada_frame.pack(fill="x")
    entrada_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)


    # Fecha y Número de Póliza
    crear_label(entrada_frame, "Fecha", FUENTE_LABEL, row=0, column=0, padx=(10, 5), pady=5, sticky="w")
    
    fecha_policia = ctk.CTkEntry(entrada_frame, placeholder_text="📅 Fecha de ingreso")
    fecha_policia= crear_entry(entrada_frame, "Fecha Póliza...", 0, 1, padx=(5, 10), pady=5, sticky="ew")
    fecha_policia.insert(0, obtener_fecha_actual())
    fecha_policia.configure(state="readonly")
    
    # No. Póliza
    crear_label(entrada_frame, "No. Póliza:", FUENTE_LABEL, row=0, column=2, padx=(10, 5), pady=5, sticky="w")
    no_poliza = crear_entry(entrada_frame, "🔢 No. Póliza", 0, 3, padx=(5, 10), pady=5, sticky="ew")

    # DATOS DEL CHEQUE
    crear_label(entrada_frame, "DATOS DEL CHEQUE", FUENTE_SECCION_TITULO, row=1, column=0, columnspan=4, pady=(15, 5), sticky="n")
    
    crear_label(entrada_frame, "Nombre", FUENTE_LABEL, row=2, column=0, padx=(10, 5), pady=5, sticky="w")
    nombre = crear_entry(entrada_frame, "👤 Nombre", 2, 1, padx=(5, 10), pady=5, sticky="ew")
    
    crear_label(entrada_frame, "Cargo", FUENTE_LABEL, row=2, column=2, padx=(10, 5), pady=5, sticky="w")
    cargo_entry = crear_entry(entrada_frame, "💰 Cargo", 2, 3, padx=(5, 10), pady=5, sticky="ew")

    crear_label(entrada_frame, "Cargo en texto", FUENTE_SECCION_TITULO, row=3, column=0, columnspan=4, pady=(15, 5), sticky="n")
    cargo_letras_entry = ctk.CTkEntry(entrada_frame, placeholder_text="💰 Cargo en letras", height=30)
    cargo_letras_entry.grid(row=4, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="ew")

    def actualizar_cargo_letras(event=None):
        valor = cargo_entry.get().strip()
        try:
            numero = float(valor)
            #cargo_letras_entry.configure(state="normal")
            cargo_letras_entry.delete(0, tk.END)
            cargo_letras_entry.insert(0, numero_a_letras_mxn(numero))
            #cargo_letras_entry.configure(state="disabled")
        except ValueError:
            ##cargo_letras_entry.configure(state="normal")
            cargo_letras_entry.delete(0, tk.END)
            #cargo_letras_entry.configure(state="disabled")

    cargo_entry.bind("<KeyRelease>", actualizar_cargo_letras)

    # RECIBÍ
    crear_label(entrada_frame, "Recibí:", FUENTE_LABEL, row=6, column=0, columnspan=4, pady=(10, 5), sticky="n")
    
    """ recibi_entry = ctk.CTkEntry(entrada_frame, placeholder_text="💰 CH", height=40)
    recibi_entry.grid(row=7, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="ew") """
    
    crear_label(entrada_frame, "Tipo de pago", FUENTE_LABEL, row=7, column=0, padx=(10, 5), pady=5, sticky="w")
    tipo_pago = ctk.CTkOptionMenu(entrada_frame, values=["EFECTIVO", "CHEQUE", "TRANSF ELECTRONICA"], width=200)
    tipo_pago.grid(row=7, column=1, padx=(5, 10), pady=5, sticky="ew")
    
    crear_label(entrada_frame, "Clave de Rastreo", FUENTE_LABEL, row=7, column=2, padx=(10, 5), pady=5, sticky="w")
    clave_rastreo = crear_entry(entrada_frame, "🔑 Clave de rastreo", 7, 3, padx=(5, 10), pady=5, sticky="ew")

    # Denominación
    crear_label(entrada_frame, "Denominación:", FUENTE_LABEL, row=8, column=0, padx=(10, 5), pady=25, sticky="w")
    denominacion_entrada = crear_entry(entrada_frame, "💵 Denominación", 8, 1, padx=(5, 10), pady=5, sticky="ew")

    # Cargo
    """ crear_label(entrada_frame, "Cargo:", FUENTE_LABEL, row=8, column=2, padx=(10, 5), pady=5, sticky="w")
    cargo_deposito = crear_entry(entrada_frame, "💰 Cargo", 8, 3, padx=(5, 10), pady=5, sticky="ew") """

    crear_label(entrada_frame, "OBSERVACIONES:", FUENTE_LABEL, row=9, column=0, columnspan=4, pady=(10, 5), sticky="n")
    observaciones_entry = ctk.CTkEntry(entrada_frame, placeholder_text="👀 OBSERVACIONES", height=40)
    observaciones_entry.grid(row=9, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="ew")

    # Sección filas adicionales
    seccion_filas = ctk.CTkFrame(contenedor_general, fg_color=FONDO_CONTENEDORES, corner_radius=15)
    seccion_filas.grid(row=10, column=0, columnspan=3, sticky="ew")

    seccion_titulos_filas = ctk.CTkFrame(contenedor_general, corner_radius=15)
    seccion_titulos_filas.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 5))

    # Column titles
    crear_label(seccion_titulos_filas, "Clave", FUENTE_SECCION_TITULO, row=0, column=0, padx=10, sticky="w")
    crear_label(seccion_titulos_filas, "Denominación", FUENTE_SECCION_TITULO, row=0, column=1, padx=10, sticky="w")
    
    
    crear_label(seccion_titulos_filas, "Cargo", FUENTE_SECCION_TITULO, row=0, column=2, padx=10, sticky="w")
    seccion_titulos_filas.grid_columnconfigure((0, 1, 2), weight=1)

    # Sección filas
    frame_filas = ctk.CTkFrame(seccion_filas, corner_radius=15)
    frame_filas.pack(fill="x")

    entradas = []

    def llenar_denominacion(event, entrada_clave, entrada_resultado):
        clave = entrada_clave.get()
        denominacion = buscar_descripcion_db(clave)
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

            importe_valor = cargo_entry.get().strip()
            if importe_valor:
                importe_float = float(importe_valor)
                if abs(importe_float - suma_total) < 0.01:
                    validacion_totales.configure(text="✅", text_color=COLOR_VALIDACION_OK)
                else:
                    validacion_totales.configure(text="❌", text_color=COLOR_VALIDACION_ERROR)
            else:
                validacion_totales.configure(text="❌", text_color=COLOR_VALIDACION_NEUTRO)
        except ValueError:
            pass

    def agregar_fila(enfocar_nueva_clave=False):
        fila_frame = ctk.CTkFrame(frame_filas, fg_color=FONDO_CONTENEDORES, corner_radius=15)
        fila_frame.pack(fill="x", pady=5)

        entrada_clave = ctk.CTkEntry(fila_frame, placeholder_text="🔑 Clave")
        entrada_clave.grid(row=0, column=0, padx=10, sticky="ew")

        entrada_resultado = ctk.CTkEntry(fila_frame, placeholder_text="Denominación", state="disabled")
        entrada_resultado.grid(row=0, column=1, padx=10, sticky="ew")

        entrada_abono = ctk.CTkEntry(fila_frame, placeholder_text="💰 Cargo")
        entrada_abono.grid(row=0, column=2, padx=10, sticky="ew")
        entrada_abono.bind("<KeyRelease>", lambda event: actualizar_total())

        entrada_clave.bind("<FocusOut>", lambda event: llenar_denominacion(event, entrada_clave, entrada_resultado))
        entrada_clave.bind("<Return>", lambda event: entrada_abono.focus_set())
        entrada_abono.bind("<Return>", lambda event: agregar_fila(enfocar_nueva_clave=True))

        btn_eliminar = ctk.CTkButton(
            fila_frame,
            text="❌",
            **btn_eliminar_style,
            command=lambda: (fila_frame.destroy(), entradas.remove((entrada_clave, entrada_resultado, entrada_abono)), actualizar_total())
        )
        btn_eliminar.grid(row=0, column=3, padx=5)

        fila_frame.grid_columnconfigure((0, 1, 2), weight=1)
        entradas.append((entrada_clave, entrada_resultado, entrada_abono))

        if enfocar_nueva_clave:
            entrada_clave.focus_set()

    agregar_fila()
    
    ctk.CTkButton(
        seccion_filas,
        text="➕ Agregar",
        command=agregar_fila,
        **btn_agregar_style
    ).pack(pady=10)


    def guardar_egrresos():
        try:
            
            app = xw.App(visible=False)
            wb = app.books.open("assets/plantillas/egresos.xlsx")
            hoja = wb.sheets["01 ene 2025"]
            
            
            fecha = fecha_policia.get()
            no_poliza_valor = no_poliza.get()
            nombre_valor = nombre.get()
            cargo_valor = cargo_entry.get()
            tipo_pago_valor = tipo_pago.get()
            clave_rastreo_valor = clave_rastreo.get()
            denominacion_valor = denominacion_entrada.get()
            observaciones_valor = observaciones_entry.get()
            print("Datos guardados:", fecha, no_poliza_valor, nombre_valor, cargo_valor, tipo_pago_valor, clave_rastreo_valor, denominacion_valor, observaciones_valor)
            
            hoja.range("AQ8").value = fecha
            hoja.range("AX5").value = no_poliza_valor
            hoja.range("A9").value = nombre_valor
            hoja.range("AO9").value = cargo_valor
            hoja.range("T12").value = tipo_pago_valor
            hoja.range("A13").value = clave_rastreo_valor
            hoja.range("A44").value = denominacion_valor
            hoja.range("A47").value = observaciones_valor
            
            fila_inicial = 18
            for i, (entrada_clave, entrada_resultado, entrada_abono) in enumerate(entradas):
                clave = entrada_clave.get()
                denominacion = entrada_resultado.get()
                cargo = entrada_abono.get()

                if clave and denominacion and cargo:
                    hoja.range(f"B{fila_inicial + i}").value = clave
                    ##hoja.range(f"B{fila_inicial + i}").value = denominacion
                    hoja.range(f"AV{fila_inicial + i}").value = float(cargo) if cargo else 0.0
                    fila_inicial += 1
                else:       
                    print("Error: Faltan datos en la fila", i + 1)
                    messagebox.showerror("Error", "Faltan datos en la fila. Verifica que todos los campos estén completos.")
                    return
                
            # Guardar el archivo
            fecha_actual = obtener_fecha_actual()
            nombre_archivo = f"Poliza_Egresos_{fecha_actual}.xlsx"
            ruta_descargas = os.path.expanduser("~/Documentos/Cecati122/PolizasDeEgresos")
            os.makedirs(ruta_descargas, exist_ok=True)
            ruta_archivo = os.path.join(ruta_descargas, nombre_archivo)
            
            wb.save(ruta_archivo)
            print("Archivo guardado en:", ruta_archivo)
            messagebox.showinfo("Éxito", f"Archivo guardado en: {ruta_archivo}")
            
            wb.save()
            wb.close()
        except Exception as e:
            print("Error al guardar:", e)
            messagebox.showerror("Error", "No se pudo guardar la información. Verifica que la plantilla esté disponible.")
            
    # Botones inferiores
    botones_frame = ctk.CTkFrame(contenedor_principal, fg_color=FONDO_CONTENEDORES, corner_radius=15)
    botones_frame.pack(fill="x", pady=10, padx=20, anchor="e")

    ctk.CTkLabel(botones_frame, text="Total:", font=FUENTE_FORMULARIO_S).pack(side="left", padx=(0, 10))
    total = ctk.CTkEntry(botones_frame, placeholder_text="💰 Total", state="readonly")
    total.pack(side="left", padx=(0, 10), fill="x", expand=False)

    validacion_totales = ctk.CTkLabel(botones_frame, text="❌", font=FUENTE_VALIDACION)
    validacion_totales.pack(side="left", padx=(0, 10))

    crear_boton_imagen(botones_frame, "Buscar", "assets/look.png", btn_guardar_style, command=lambda: abrir_carpeta("assets/plantillas/egresos.xlsx"), side="right", padx=10)
    crear_boton_imagen(botones_frame, "Guardar", "assets/check.png", btn_guardar_style, None, side="right", padx=10)
    crear_boton_imagen(botones_frame, "Descargar", "assets/downlo.png", btn_descargar_style, guardar_egrresos, side="right", padx=10)