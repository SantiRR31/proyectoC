import tkinter as tk
import customtkinter as ctk
from functions.funcions import obtener_fecha_actual, buscar_denominacion_db
from db.egresosDB import buscar_descripcion_db
from widgets.widgets import *
from styles.styles import *
from utils.config_utils import cargar_config
CONFIG_PATH = "config.json"

#Entradas de arriba del documento
#clave_cecati = '22DBT0005P'
n_cuenta_cheques = 1056897860
fecha_elaboracion = obtener_fecha_actual()
#periodo_informe = False


def mostrar_informe_real_ingresos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()
        
    config = cargar_config()
        
    # Título principal
    ctk.CTkLabel(frame_padre, text="Informe Real de Ingresos", font=FUENTE_FORMULARIO_T).pack(pady=30)

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
    
    # Denominación
    crear_label(entrada_frame, "Clave Cecati:", FUENTE_LABEL, row=6, column=0, padx=(10, 5), pady=25, sticky="w")
    clav_cecati = crear_entry(entrada_frame, config.get("clave_cecati", '22DBT0005P'), 6, 1, padx=(5, 10), pady=5, sticky="ew")
    clav_cecati.insert(0, config.get("clave_cecati", '22DBT0005P'))
    
    # Cargo
    crear_label(entrada_frame, "No. Cuenta Cheques:", FUENTE_LABEL, row=6, column=2, padx=(10, 5), pady=5, sticky="w")
    cta_cheques = crear_entry(entrada_frame, n_cuenta_cheques, 6, 3, padx=(5, 10), pady=5, sticky="ew")
    cta_cheques.insert(0, n_cuenta_cheques)

    # Folio
    crear_label(entrada_frame, "Fecha de elaboración:", FUENTE_LABEL, row=6, column=4, padx=(10, 5), pady=5, sticky="w")
    fecha_elab = crear_entry(entrada_frame, fecha_elaboracion, 6, 5, padx=(5, 10), pady=5, sticky="ew")
    fecha_elab.insert(0, obtener_fecha_actual())
    fecha_elab.configure(state="readonly")

    # Referencia
    crear_label(entrada_frame, "Periodo Informe:", FUENTE_LABEL, row=6, column=6, padx=(10, 5), pady=5, sticky="w")
    referencia = crear_entry(entrada_frame, "Periodo de informe", 6, 7, padx=(5, 10), pady=5, sticky="ew")
    
    # Subtotal
    crear_label(entrada_frame, "Subtotal:", FUENTE_LABEL, row=7, column=6, padx=(10, 5), pady=(15, 5), sticky="e")
    subtotal = crear_entry(entrada_frame, "Subtotal", 7, 7, padx=(5, 10), pady=(15, 5), sticky="ew")


    seccion_titulos_filas = ctk.CTkFrame(contenedor_general, corner_radius=15)
    seccion_titulos_filas.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 5))
    
    # Sección filas adicionales
    seccion_filas = ctk.CTkFrame(contenedor_general, fg_color=FONDO_CONTENEDORES, corner_radius=15)
    seccion_filas.grid(row=9, column=0, columnspan=3, sticky="ew")
    
    # Column titles
    crear_label(seccion_titulos_filas, "Clave", FUENTE_SECCION_TITULO, row=0, column=0, padx=10, sticky="w")
    crear_label(seccion_titulos_filas, "Descripción", FUENTE_SECCION_TITULO, row=0, column=1, padx=10, sticky="w")
    crear_label(seccion_titulos_filas, "Importes", FUENTE_SECCION_TITULO, row=0, column=2, padx=10, sticky="w")
    seccion_titulos_filas.grid_columnconfigure(0, weight=1)  # Clave
    seccion_titulos_filas.grid_columnconfigure(1, weight=2)  # Descripción
    seccion_titulos_filas.grid_columnconfigure(2, weight=3)  # Importes

    

    
    # Sección filas
    frame_filas = ctk.CTkFrame(seccion_filas, corner_radius=15)
    frame_filas.pack(fill="x")

    entradas = []
    
    
    def llenar_denominacion(event, entrada_clave, entrada_resultado):
        clave = entrada_clave.get()
        denominacion = buscar_denominacion_db(clave)
        if denominacion == 'No encontrada':
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

            importe_valor = subtotal.get().strip()
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
        
        entrada_subgrupo = ctk.CTkEntry(fila_frame, placeholder_text="Subgrupo")
        entrada_subgrupo.grid(row=0, column=2, padx=10, sticky="ew")
        entrada_grupo = ctk.CTkEntry(fila_frame, placeholder_text="Grupo")
        entrada_grupo.grid(row=0, column=3, padx=10, sticky="ew")
        entrada_grupo.bind("<KeyRelease>", lambda event: actualizar_total())

        entrada_clave.bind("<FocusOut>", lambda event: llenar_denominacion(event, entrada_clave, entrada_resultado))
        entrada_clave.bind("<Return>", lambda event: entrada_subgrupo.focus_set())
        entrada_subgrupo.bind("<Return>", lambda event: entrada_grupo.focus_set())
        entrada_grupo.bind("<Return>", lambda event: agregar_fila(enfocar_nueva_clave=True))

        btn_eliminar = ctk.CTkButton(
            fila_frame,
            text="❌",
            **btn_eliminar_style,
            command=lambda: (fila_frame.destroy(), entradas.remove((entrada_clave, entrada_resultado, entrada_subgrupo, entrada_grupo)), actualizar_total())
        )
        btn_eliminar.grid(row=0, column=4, padx=(10,5))

        fila_frame.grid_columnconfigure(0, weight=1)  # Clave
        fila_frame.grid_columnconfigure(1, weight=4)  # Denominación (más ancho)
        fila_frame.grid_columnconfigure(2, weight=1)  # Subgrupo (más estrecho)
        fila_frame.grid_columnconfigure(3, weight=1)  # Cargo (más estrecho)
        fila_frame.grid_columnconfigure(4, weight=0)  # Botón eliminar

        
        entradas.append((entrada_clave, entrada_resultado, entrada_subgrupo, entrada_grupo))

        if enfocar_nueva_clave:
            entrada_clave.focus_set()

    agregar_fila()

    ctk.CTkButton(
        seccion_filas,
        text="➕ Agregar",
        command=agregar_fila,
        **btn_agregar_style
    ).pack(pady=10)
    
    # Botones inferiores
    botones_frame = ctk.CTkFrame(contenedor_principal, fg_color=FONDO_CONTENEDORES, corner_radius=15)
    botones_frame.pack(fill="x", pady=10, padx=20, anchor="e")

    ctk.CTkLabel(botones_frame, text="Total:", font=FUENTE_FORMULARIO_S).pack(side="left", padx=(0, 10))
    total = ctk.CTkEntry(botones_frame, placeholder_text="💰 Total", state="readonly")
    total.pack(side="left", padx=(0, 10), fill="x", expand=False)

    validacion_totales = ctk.CTkLabel(botones_frame, text="❌", font=FUENTE_VALIDACION)
    validacion_totales.pack(side="left", padx=(0, 10))

    crear_boton_imagen(botones_frame, "Ver Descargas", "assets/look.png", btn_guardar_style, None, side="right", padx=10)
    crear_boton_imagen(botones_frame, "Descargar", "assets/downlo.png", btn_descargar_style, None, side="right", padx=10)