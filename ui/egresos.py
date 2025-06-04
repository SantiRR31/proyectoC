import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import xlwings as xw
from db.egresosDB import *
from tkcalendar import DateEntry
from widgets.widgets import *
from utils.utils import *
from utils.egresos_utils import *
from datetime import datetime
from styles.styles import *

def mostrar_formulario_egresos(frame_padre):
    # Limpiar frame anterior
    for widget in frame_padre.winfo_children():
        widget.destroy()

    # Contenedor principal con scroll
    contenedor_principal = ctk.CTkScrollableFrame(
        frame_padre, 
        fg_color="transparent"
    )
    contenedor_principal.pack(fill="both", expand=True, padx=20, pady=10)

    # Título principal con sombra sutil
    titulo_frame = ctk.CTkFrame(contenedor_principal, fg_color="transparent")
    titulo_frame.pack(fill="x", pady=(0, 20))
    
    ctk.CTkLabel(
        titulo_frame,
        text="Póliza de Egresos",
        font=FUENTE_TITULO,
        text_color=TEXT_PRIMARY
    ).pack(side="left")

    # Sección de datos de la póliza
    seccion_poliza = ctk.CTkFrame(contenedor_principal, **ESTILO_FRAME)
    seccion_poliza.pack(fill="x", pady=(0, 20), padx=5)

    # Haz todas las columnas responsivas
    for i in range(4):
        seccion_poliza.grid_columnconfigure(i, weight=1, uniform="poliza")

    # Fila 1: Fecha y Número de Póliza
    ctk.CTkLabel(
        seccion_poliza,
        text="Fecha:",
        font=FUENTE_LABEL,
        anchor="w"
    ).grid(row=0, column=0, padx=(15, 5), pady=10, sticky="ew")

    fecha_policia = DateEntry(
        seccion_poliza,
        date_pattern="dd/mm/yyyy",
        font=FUENTE_TEXTO,
        locale="es_MX",
        background="#3b82f6",
        foreground="white",
        borderwidth=1
    )
    fecha_policia.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

    ctk.CTkLabel(
        seccion_poliza,
        text="No. Póliza:",
        font=FUENTE_LABEL,
        anchor="w"
    ).grid(row=0, column=2, padx=(15, 5), pady=10, sticky="ew")

    no_poliza = ctk.CTkEntry(
        seccion_poliza,
        placeholder_text="🔢 No. Póliza",
        **ESTILO_ENTRADA
    )
    no_poliza.grid(row=0, column=3, padx=(5, 15), pady=10, sticky="ew")

    # Separador visual
    separador = ctk.CTkFrame(
        seccion_poliza,
        height=2,
        fg_color=("#e5e7eb", "#191919")
    )
    separador.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)

    # Fila 2: Datos del beneficiario
    ctk.CTkLabel(
        seccion_poliza,
        text="DATOS DEL BENEFICIARIO",
        font=FUENTE_SUBTITULO,
        anchor="center"
    ).grid(row=2, column=0, columnspan=4, pady=(10, 5), sticky="ew")

    ctk.CTkLabel(
        seccion_poliza,
        text="Nombre:",
        font=FUENTE_LABEL,
        anchor="w"
    ).grid(row=3, column=0, padx=(15, 5), pady=5, sticky="ew")

    vcmdo = seccion_poliza.register(solo_letras)
    nombre = ctk.CTkEntry(
        seccion_poliza,
        placeholder_text="👤 Nombre completo",
        **ESTILO_ENTRADA
    )
    nombre.configure(validate="key", validatecommand=(vcmdo, "%P"))
    nombre.bind("<KeyRelease>", lambda event: convertir_a_mayusculas(nombre, event))
    nombre.grid(row=3, column=1, columnspan=3, padx=(5, 15), pady=5, sticky="ew")

# Fila 3: Monto y descripción
    ctk.CTkLabel(
        seccion_poliza,
        text="Monto:",
        font=FUENTE_LABEL,
        anchor="w"
    ).grid(row=4, column=0, padx=(15, 5), pady=5, sticky="ew")

    cargo_entry = ctk.CTkEntry(
        seccion_poliza,
        placeholder_text="💰 Cantidad en números",
        **ESTILO_ENTRADA
    )
    vcmd = seccion_poliza.register(solo_numeros_decimales)
    cargo_entry.configure(validate="key", validatecommand=(vcmd, "%P"))
    cargo_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

    ctk.CTkLabel(
        seccion_poliza,
        text="Monto en letras:",
        font=FUENTE_LABEL,
        anchor="w"
    ).grid(row=4, column=2, padx=(15, 5), pady=5, sticky="ew")

    cargo_letras_entry = ctk.CTkEntry(
        seccion_poliza,
        placeholder_text="💰 Cantidad en letras",
        state="disabled",
        **ESTILO_ENTRADA
    )
    cargo_letras_entry.grid(row=4, column=3, padx=(5, 15), pady=5, sticky="ew")

    def actualizar_cargo_letras(event=None):
        valor = cargo_entry.get().strip()
        try:
            numero = float(valor)
            cargo_letras_entry.configure(state="normal")
            cargo_letras_entry.delete(0, tk.END)
            cargo_letras_entry.insert(0, numero_a_letras_mxn(numero))
            cargo_letras_entry.configure(state="disabled")
        except ValueError:
            cargo_letras_entry.configure(state="normal")
            cargo_letras_entry.delete(0, tk.END)
            cargo_letras_entry.configure(state="disabled")

    cargo_entry.bind("<KeyRelease>", actualizar_cargo_letras)

    # Sección de método de pago
    metodo_pago_frame = ctk.CTkFrame(contenedor_principal, **ESTILO_FRAME)
    metodo_pago_frame.pack(fill="x", pady=(0, 20), padx=5)

# Configura las columnas para que sean responsivas
    for i in range(4):
        metodo_pago_frame.grid_columnconfigure(i, weight=1, uniform="metodo_pago")

    ctk.CTkLabel(
        metodo_pago_frame,
        text="MÉTODO DE PAGO",
        font=FUENTE_SUBTITULO
    ).grid(row=0, column=0, columnspan=4, pady=(5, 10), sticky="ew")

    # Elementos de método de pago
    ctk.CTkLabel(
        metodo_pago_frame,
        text="Tipo de pago:",
        font=FUENTE_LABEL,
        anchor="w"
    ).grid(row=1, column=0, padx=(15, 5), pady=5, sticky="ew")

    tipo_pago = ctk.CTkOptionMenu(
        metodo_pago_frame,
        values=["EFECTIVO", "CHEQUE", "TRANSF. ELECTRÓNICA"],
        font=FUENTE_TEXTO,
        dropdown_font=FUENTE_TEXTO,
        width=200
    )
    tipo_pago.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ctk.CTkLabel(
        metodo_pago_frame,
        text="Clave/Referencia:",
        font=FUENTE_LABEL,
        anchor="w"
    ).grid(row=1, column=2, padx=(15, 5), pady=5, sticky="ew")

    clave_rastreo = ctk.CTkEntry(
        metodo_pago_frame,
        placeholder_text="🔑 Clave de rastreo",
        **ESTILO_ENTRADA
    )
    clave_rastreo.configure(validate="key", validatecommand=(vcmdo, "%P"))
    clave_rastreo.bind("<KeyRelease>", lambda event: convertir_a_mayusculas(clave_rastreo, event))
    clave_rastreo.grid(row=1, column=3, padx=(5, 15), pady=5, sticky="ew")
    
    
    
    #-----------------------------------------------------------# Sección de conceptos -------------------------------------------------------------------------------------------
    
    
    
    
    conceptos_frame = ctk.CTkFrame(contenedor_principal, **ESTILO_FRAME)
    conceptos_frame.pack(fill="x", pady=(0, 20), padx=5)

    ctk.CTkLabel(
        conceptos_frame,
        text="CONCEPTOS",
        font=FUENTE_SUBTITULO
    ).grid(row=0, column=0, columnspan=4, pady=(5, 10))

    # Encabezados de tabla
    encabezados = ["Clave", "Descripción", "Importe"]
    for col, texto in enumerate(encabezados):
        ctk.CTkLabel(
            conceptos_frame,
            text=texto,
            font=FUENTE_LABEL,
            anchor="w"
        ).grid(row=1, column=col, padx=10, pady=(0, 5), sticky="ew")

    # Reemplaza la creación de filas_frame con esto:
    filas_frame = ctk.CTkScrollableFrame(
        conceptos_frame,
        height=180,
        fg_color="transparent",
        #scrollbar_fg_color="transparent"
        #fg_color="transparent",
        scrollbar_fg_color=("#e5e7eb", "#374151"),
        scrollbar_button_color=("#9ca3af", "#4b5563"),
        scrollbar_button_hover_color=("#6b7280", "#374151")
    )

    # Configuración de grid
    filas_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=(0, 10))

    # Bloqueo de eventos de scroll
    filas_frame.bind("<Enter>", lambda e: filas_frame.focus_set())
    for event in ["<MouseWheel>", "<Button-4>", "<Button-5>"]:
        filas_frame.bind(event, lambda e: "break")

    # Configuración de pesos
    conceptos_frame.grid_rowconfigure(2, weight=1)
    for i in range(4):
        conceptos_frame.grid_columnconfigure(i, weight=1 if i < 3 else 0)



    entradas = []
       

    def llenar_denominacion(event, entrada_clave, entrada_resultado):
        clave = entrada_clave.get()
        denominacion = buscar_descripcion_db(clave)
        entrada_resultado.configure(state="normal")
        entrada_resultado.delete(0, tk.END)
        entrada_resultado.insert(0, denominacion)
        entrada_resultado.configure(state="readonly")
        
        
    def llenar_por_clave(event, entrada_clave, entrada_desc):
        clave = entrada_clave.get().strip()
        if clave:
            descripcion = buscar_descripcion_db(clave)
            entrada_desc.configurate(state= "normal")
            entrada_desc.delete(0, tk.end)
            entrada_desc.insert(0, descripcion)
            entrada_desc.configure(state="readonly")
    
    def llenar_por_descripcion(event, entrada_desc, entrada_clave):
        descripcion = entrada_desc.get().strip()
        if descripcion:
            clave = buscar_clave_por_descripcion(descripcion)
            entrada_clave.delete(0, tk.END)
            entrada_clave.insert(0, clave)
            

    def actualizar_total():
        try:
            suma_total = sum(float(entrada[2].get()) for entrada in entradas if entrada[2].get().strip())
            total.configure(state="normal")
            total.delete(0, tk.END)
            total.insert(0, f"${suma_total:,.2f}")
            total.configure(state="readonly")
        
        # Validación visual mejorada
            importe_valor = cargo_entry.get().strip()
            if importe_valor:
                importe_float = float(importe_valor)
                diferencia = abs(importe_float - suma_total)
            
                if diferencia < 0.01:
                    validacion_totales.configure(
                        text="✓ Totales coinciden",
                        text_color="#10b981",
                        font=("Arial", 10, "bold")
                    )
                else:
                    validacion_totales.configure(
                        text=f"✗ Diferencias (${diferencia:,.2f})",
                        text_color="#ef4444",
                        font=("Arial", 10, "bold")
                    )
            else:
                validacion_totales.configure(
                    text="⚠ Ingrese monto total",
                    text_color="#f59e0b",
                    font=("Arial", 10)
                )
        except ValueError:
            validacion_totales.configure(
                text="⚠ Valores no válidos",
                text_color="#f59e0b",
                font=("Arial", 10)
            )
    
    def mostrar_sugerencias(event, entrada_desc, entrada_clave, lista_sugerencias):
        texto = entrada_desc.get().strip()
        coincidencias = buscar_claves_por_texto(texto)
        lista_sugerencias.delete(0, tk.END)
    
        if coincidencias:
            for clave, descripcion in coincidencias:
                lista_sugerencias.insert(tk.END, f"{clave} - {descripcion}")
        else:
            lista_sugerencias.insert(tk.END, "No se encontraron coincidencias")
    
    # Mostrar lista justo debajo de la entrada
        lista_sugerencias.place(in_=entrada_desc, relx=0, rely=1.0, relwidth=1.0)

    
    def seleccionar_sugerencia(event, entrada_clave, entrada_desc, lista_sugerencias):
        seleccion = lista_sugerencias.get(tk.ACTIVE)
        if " - " in seleccion:
            clave, descripcion = seleccion.split(" - ", 1)
            entrada_clave.delete(0, tk.END)
            entrada_clave.insert(0, clave)
            entrada_desc.delete(0, tk.END)
            entrada_desc.insert(0, descripcion)
        lista_sugerencias.place_forget()
       

    def agregar_fila(enfocar_nueva_clave=False):
        fila_idx = len(entradas)
        
        fila_frame = ctk.CTkFrame(
            filas_frame, 
            fg_color=("#ffffff", "#1f2937"),
            border_width=1,
            border_color=("#e5e7eb", "#374151"),
            corner_radius=6
            )
        fila_frame.pack(fill="x", pady=2, padx=2)
        
        
         # Efecto hover
        def on_enter(e):
            fila_frame.configure(fg_color=("#f3f4f6", "#111827"))
        def on_leave(e):
            fila_frame.configure(fg_color=("#ffffff", "#1f2937"))
        fila_frame.bind("<Enter>", on_enter)
        fila_frame.bind("<Leave>", on_leave)

        fila_frame.columnconfigure(0, weight=2, uniform="fila")
        fila_frame.columnconfigure(1, weight=4, uniform="fila")
        fila_frame.columnconfigure(2, weight=2, uniform="fila")
        fila_frame.columnconfigure(3, weight=0)
        
        
        # Entrada clave
        entrada_clave = ctk.CTkEntry(
            fila_frame,
            placeholder_text="Ej. 4100",
            width=120,
            **ESTILO_ENTRADA
        )
        entrada_clave.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Entrada descripción
        entrada_desc = ctk.CTkEntry(
            fila_frame,
            placeholder_text="Descripción",
            **ESTILO_ENTRADA
        )
        entrada_desc.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        # Entrada importe
        entrada_importe = ctk.CTkEntry(
            fila_frame,
            placeholder_text="💰 Importe",
            **ESTILO_ENTRADA
        )
        lista_sugerencias = tk.Listbox(
            conceptos_frame,
            height=4,
            bg="#ffffff",
            fg="#111827",
            selectbackground="#3b82f6",
            font=("Arial", 10),
            relief="flat"
        )
        lista_sugerencias.bind("<<ListboxSelect>>", lambda e: seleccionar_sugerencia(e, entrada_clave, entrada_desc, lista_sugerencias))
        entrada_desc.bind("<KeyRelease>", lambda e: mostrar_sugerencias(e, entrada_desc, entrada_clave, lista_sugerencias))

        
        vcmd = fila_frame.register(solo_numeros_decimales)
        entrada_importe.configure(validate="key", validatecommand=(vcmd, "%P"))
        entrada_importe.bind("<KeyRelease>", lambda event: actualizar_total())
        entrada_importe.grid(row=0, column=2, padx=5, pady=2, sticky="ew")
        entrada_clave.bind("<FocusOut>", lambda event: llenar_por_clave(event, entrada_clave, entrada_desc))
        entrada_desc.bind("<FocusOut>", lambda event: llenar_por_descripcion(event, entrada_desc, entrada_clave))
        entrada_clave.bind("<Return>", lambda event: entrada_importe.focus_set())
        entrada_importe.bind("<Return>", lambda event: agregar_fila(enfocar_nueva_clave=True))


        # Botón eliminar
        btn_eliminar = ctk.CTkButton(
            fila_frame,
            text="✕",
            width=30,
            height=30,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=lambda: (fila_frame.destroy(), entradas.remove((entrada_clave, entrada_desc, entrada_importe)), actualizar_total())
        )
        btn_eliminar.grid(row=0, column=3, padx=5, pady=2)

        # Configurar eventos
        entrada_clave.bind("<FocusOut>", lambda event: llenar_denominacion(event, entrada_clave, entrada_desc))
        entrada_clave.bind("<Return>", lambda event: entrada_importe.focus_set())
        entrada_importe.bind("<Return>", lambda event: agregar_fila(enfocar_nueva_clave=True))

        entradas.append((entrada_clave, entrada_desc, entrada_importe))

        if enfocar_nueva_clave:
            entrada_clave.focus_set()

    # Agregar primera fila por defecto
    agregar_fila()

    # Botón para agregar más filas
    ctk.CTkButton(
        conceptos_frame,
        text="➕ Agregar concepto",
        **ESTILO_BOTON,
        fg_color="#3b82f6",
        hover_color="#2563eb",
        command=agregar_fila
    ).grid(row=3, column=0, columnspan=4, pady=10)
    
     # Sección de observaciones
    denominacion_frame = ctk.CTkFrame(contenedor_principal, **ESTILO_FRAME)
    denominacion_frame.pack(fill="x", pady=(0, 20), padx=5)

    ctk.CTkLabel(
        denominacion_frame,
        text="DENOMINACION",
        font=FUENTE_SUBTITULO
    ).pack(pady=(5, 10))

    denominacion_entry = ctk.CTkEntry(
        denominacion_frame,
        placeholder_text="Escriba aquí cualquier observación adicional...",
        #height=40,
        **ESTILO_ENTRADA
    )
    denominacion_entry.pack(fill="x", padx=10, pady=(0, 10))
    denominacion_entry.bind("<KeyRelease>", lambda event: convertir_a_mayusculas(denominacion_entry, event))





#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

 
    # Sección de observaciones
    observaciones_frame = ctk.CTkFrame(contenedor_principal, **ESTILO_FRAME)
    observaciones_frame.pack(fill="x", pady=(0, 20), padx=5)

    ctk.CTkLabel(
        observaciones_frame,
        text="OBSERVACIONES",
        font=FUENTE_SUBTITULO
    ).pack(pady=(5, 10))

    observaciones_entry = ctk.CTkEntry(
        observaciones_frame,
        placeholder_text="Escriba aquí cualquier observación adicional...",
        #height=40,
        **ESTILO_ENTRADA
    )
    observaciones_entry.pack(fill="x", padx=10, pady=(0, 10))
    observaciones_entry.bind("<KeyRelease>", lambda event: convertir_a_mayusculas(observaciones_entry, event))

    # Barra de acciones inferiores
    acciones_frame = ctk.CTkFrame(
        contenedor_principal, 
        fg_color="transparent")
    acciones_frame.pack(fill="x", pady=(10, 0))

    # Total y validación
    ctk.CTkLabel(
        acciones_frame,
        text="Total:",
        font=FUENTE_LABEL
    ).pack(side="left", padx=(0, 10))

    total = ctk.CTkEntry(
        acciones_frame,
        width=150,
        state="readonly",
        font=FUENTE_TEXTO,
        justify="right"
    )
    total.pack(side="left", padx=(0, 10))

    validacion_totales = ctk.CTkLabel(
        acciones_frame,
        text="?",
        font=("Arial", 16, "bold"),
        text_color="#6b7280"
    )
    validacion_totales.pack(side="left", padx=(0, 20))

    # Botones de acción
    btn_guardar = ctk.CTkButton(
        acciones_frame,
        text="💾 Guardar",
        **ESTILO_BOTON,
        fg_color="#10b981",
        hover_color="#059669",
        command=lambda: ejecutar_con_loading(
        guardar_egresos,           # función a ejecutar
        btn_guardar,               # botón guardar
        btn_descargar,             # botón descargar
        contenedor_principal,      # contenedor principal
        limpiar_formulario,        # función para limpiar el formulario
        form, entradas             # argumentos para guardar_egresos
    )
    )
    btn_guardar.pack(side="right", padx=5)

    btn_descargar = ctk.CTkButton(
        acciones_frame,
        text="📥 Descargar",
        **ESTILO_BOTON,
        fg_color="#3b82f6",
        hover_color="#2563eb",
        command=lambda: mostrar_menu_descarga(form, entradas)
    )
    btn_descargar.pack(side="right", padx=5)

    btn_buscar = ctk.CTkButton(
        acciones_frame,
        text="🔍 Buscar",
        **ESTILO_BOTON,
        fg_color="#6b7280",
        hover_color="#4b5563",
        command=lambda: abrir_carpeta("~/Documentos/Cecati122/PolizasDeIngresos")
    )
    btn_buscar.pack(side="right", padx=5)

    # Diccionario con los campos del formulario
    form = {
        "fecha": fecha_policia,
        "no_poliza": no_poliza,
        "nombre": nombre,
        "cargo": cargo_entry,
        "cargo_letras": cargo_letras_entry,
        "tipo_pago": tipo_pago,
        "clave_rastreo": clave_rastreo,
        "observaciones": observaciones_entry,
        "denominacion": denominacion_entry,
    }

    # Función para mostrar menú de descarga
   # Supón que tienes estas referencias en tu función principal:
# btn_guardar, btn_descargar, contenedor_principal, form, entradas, mostrar_formulario_egresos, frame_padre

    def mostrar_menu_descarga(form, entradas):
        menu = tk.Menu(None, tearoff=0)
        menu.add_command(
            label="Exportar como PDF",
            command=lambda: ejecutar_con_loading(
                guardar_pdf,
                btn_guardar,
                btn_descargar,
                contenedor_principal,
                lambda: limpiar_formulario(contenedor_principal, mostrar_formulario_egresos, frame_padre),
                form, entradas
            )
        )
        menu.add_command(
            label="Exportar como Excel",
            command=lambda: ejecutar_con_loading(
                guardar_egresos,
                btn_guardar,
                btn_descargar,
                contenedor_principal,
                lambda: limpiar_formulario(contenedor_principal, mostrar_formulario_egresos, frame_padre),
                form, entradas
            )
        )
    # Posicionar el menú cerca del botón
        try:
            x = btn_descargar.winfo_rootx()
            y = btn_descargar.winfo_rooty() + btn_descargar.winfo_height()
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()

    # Función para validar campos obligatorios
    def campos_obligatorios_vacios():
        campos = [
            nombre,
            cargo_entry,
            clave_rastreo,
            observaciones_entry
        ]
        return any(campo.get().strip() == "" for campo in campos)

    def actualizar_estado_botones(event=None):
        if campos_obligatorios_vacios():
            btn_guardar.configure(state="disabled")
            btn_descargar.configure(state="disabled")
        else:
            btn_guardar.configure(state="normal")
            btn_descargar.configure(state="normal")

    # Configurar eventos para validación en tiempo real
    for campo in [nombre, cargo_entry, clave_rastreo, observaciones_entry]:
        campo.bind("<KeyRelease>", actualizar_estado_botones)

    # Validación inicial
    actualizar_estado_botones()
    actualizar_total()
    
    
    ## Funciones 
    
    
    