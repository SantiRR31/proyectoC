import tkinter as tk
import customtkinter as ctk
from functions.genRegIngresos import confirmar_y_generar
from informes.poliza import guardar_egresos, guardar_pdf
from utils.rutas import ruta_absoluta
from db.egresosDB import *
from tkcalendar import DateEntry
from widgets.widgets import *
from utils.utils import *
from utils.egresos_utils import *
from styles.styles import *
from models.egresomodelos import *
CONFIG_PATH = ruta_absoluta("config.json")
config = cargar_config()

numero_generado_anterior = None
no_poliza_autogenerado = None 

def mostrar_formulario_egresos(frame_padre, poliza_editar=None):
    es_edicion = poliza_editar is not None
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
    
    # Título a la izquierda
    ctk.CTkLabel(
        titulo_frame,
        text="Póliza de Egresos",
        font=FUENTE_TITULO,
        text_color=TEXT_PRIMARY
    ).pack(side="left", padx=(10, 0))

    # Sección de datos de la póliza
    seccion_poliza = ctk.CTkFrame(contenedor_principal, **ESTILO_FRAME)
    seccion_poliza.pack(fill="x", pady=(0, 20), padx=5)

    # Haz todas las columnas responsivas
    for i in range(5):
        seccion_poliza.grid_columnconfigure(i, weight=1, uniform="poliza")

    entrada_id = ctk.CTkEntry(contenedor_principal)
    entrada_id.pack_forget()  # siempre oculto

    if poliza_editar:
        entrada_id.insert(0, str(poliza_editar.poliza_id))
        entrada_id.configure(state="disabled")  # opcional: deshabilitar

    # Fila 1: Fecha y Número de Póliza
    ctk.CTkLabel(
        seccion_poliza,
        text="Fecha:",
        font=FUENTE_LABEL,
        anchor="w"
    ).grid(row=0, column=0, padx=(15, 5), pady=10, sticky="ew")
    
    fecha_policia = DateEntry(
        seccion_poliza,
        **ESTILO_DATEENTRY
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
    no_poliza.grid(row=0, column=3, padx=(5, 5), pady=10, sticky="ew")
    
    def on_focus_out_no_poliza(event):
        valor_actual = no_poliza.get().strip()
        if valor_actual:
            valor_formateado = formatear_numero_poliza(valor_actual)
            no_poliza.delete(0, "end")
            no_poliza.insert(0, valor_formateado)

    no_poliza.bind("<FocusOut>", on_focus_out_no_poliza)



    sufijo_fecha = ctk.CTkEntry(
        seccion_poliza,
        placeholder_text="/mes/año",
        state="readonly",  # solo lectura
        **ESTILO_ENTRADA
    )
    sufijo_fecha.grid(row=0, column=4, padx=(0, 15), pady=10, sticky="ew")

     # <--- Agrega esta línea aquí

    def actualizar_no_poliza(event=None):
        global no_poliza_autogenerado

        fecha = fecha_policia.get()
        valor_completo = generar_no_poliza_para_fecha(fecha)  # Ej: "03/jul/2025"

        if "/" in valor_completo:
            numero_generado, sufijo = valor_completo.split("/", 1)
            sufijo = "/" + sufijo
        else:
            numero_generado = valor_completo
            sufijo = ""

        valor_actual = no_poliza.get().strip()

        if valor_actual == no_poliza_autogenerado or not valor_actual:
            # Solo autocompletar si está vacío o aún contiene el valor generado anterior
            no_poliza.delete(0, "end")
            no_poliza.insert(0, numero_generado)
            no_poliza_autogenerado = numero_generado  # Se guarda como autogenerado
        else:
            # El usuario escribió manualmente algo diferente
            valor_formateado = formatear_numero_poliza(valor_actual)
            no_poliza.delete(0, "end")
            no_poliza.insert(0, valor_formateado)
            # Y *no* actualizamos `no_poliza_autogenerado` aquí

        # Actualizar el sufijo
        sufijo_fecha.configure(state="normal")
        sufijo_fecha.delete(0, "end")
        sufijo_fecha.insert(0, sufijo)
        sufijo_fecha.configure(state="readonly")


    if not es_edicion:
        actualizar_no_poliza()
        fecha_policia.bind("<<DateEntrySelected>>", actualizar_no_poliza)

    # Separador visual
    separador = ctk.CTkFrame(
        seccion_poliza,
        height=2,
        fg_color=("#e5e7eb", "#191919")
    )
    separador.grid(row=1, column=0, columnspan=4, sticky="ew", pady=5)
    
#    -------------------------------------------------------------------------------------------------------

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

    def convertir_a_mayusculas(event):
        widget = event.widget  # <--- aquí accedes al widget que perdió el foco
        texto = widget.get()
        widget.delete(0, "end")
        widget.insert(0, texto.upper())

    nombre = ctk.CTkEntry(
        seccion_poliza,
        placeholder_text="👤 Nombre completo",
        **ESTILO_ENTRADA
    )
    nombre.configure(validate="key")
    # Convertir a mayúsculas mientras se escribe
    nombre.configure(validate="key")
    # Convertir a mayúsculas solo al perder el foco
    nombre.bind("<FocusOut>", convertir_a_mayusculas)
    nombre.grid(row=3, column=1, columnspan=3, padx=(5, 15), pady=5, sticky="ew")

    
# Etiqueta "Monto"
    ctk.CTkLabel(
        seccion_poliza,
        text="Monto:",
        font=FUENTE_LABEL,
        anchor="w"
    ).grid(row=4, column=0, padx=(15, 5), pady=5, sticky="ew")

# Entrada de cantidad numérica
    cargo_entry = ctk.CTkEntry(
        seccion_poliza,
        placeholder_text="💰 Cantidad en números",
        **ESTILO_ENTRADA
    )
    vcmd = seccion_poliza.register(solo_numeros_decimales)
    cargo_entry.configure(validate="key", validatecommand=(vcmd, "%P"))
    cargo_entry.bind("<KeyRelease>", lambda event: actualizar_total(entradas, total, cargo_entry, validacion_totales, total, total_ctk))
    cargo_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

# Entrada de cantidad en letras (más ancha)
    cargo_letras_entry = ctk.CTkEntry(
        seccion_poliza,
        placeholder_text="💰 Cantidad en letras",
        state="disabled",
        **ESTILO_ENTRADA
    )
    cargo_letras_entry.grid(row=4, column=2, columnspan=2, padx=(5, 15), pady=5, sticky="ew")

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
        values=["", "CHEQUE", "TRANSF. ELECTRÓNICA"],
        font=FUENTE_TEXTO,
        dropdown_font=FUENTE_TEXTO,
        width=200
    )
    tipo_pago.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Etiqueta y entrada para "No. Cheque"
    no_cheque_label = ctk.CTkLabel(
        metodo_pago_frame,
        text="No. Cheque:",
        font=FUENTE_LABEL,
        anchor="w"
    )
    no_cheque_entry = ctk.CTkEntry(
        metodo_pago_frame,
        placeholder_text="🔢 No. Cheque",
        **ESTILO_ENTRADA
    )

    # Etiqueta y entrada para "Clave/Referencia"
    clave_ref_label = ctk.CTkLabel(
        metodo_pago_frame,
        text="Clave/Referencia:",
        font=FUENTE_LABEL,
        anchor="w"
    ) 
    clave_rastreo = ctk.CTkEntry(
    metodo_pago_frame,
    placeholder_text="🔑 Clave de rastreo",
    **ESTILO_ENTRADA
    )
    #clave_rastreo.configure(validate="key", validatecommand=(vcmdo, "%P"))
    clave_rastreo.bind("<KeyRelease>", lambda event: convertir_a_mayusculas(clave_rastreo, event))

    def mostrar_campos_pago():
        # Ocultar ambos primero
        no_cheque_label.grid_forget()
        no_cheque_entry.grid_forget()
        clave_ref_label.grid_forget()
        clave_rastreo.grid_forget()

        if tipo_pago.get() == "CHEQUE":
            no_cheque_label.grid(row=1, column=2, padx=(15, 5), pady=5, sticky="ew")
            no_cheque_entry.grid(row=1, column=3, padx=(5, 15), pady=5, sticky="ew")
        elif tipo_pago.get() == "TRANSF. ELECTRÓNICA":
            clave_ref_label.grid(row=1, column=2, padx=(15, 5), pady=5, sticky="ew")
            clave_rastreo.grid(row=1, column=3, padx=(5, 15), pady=5, sticky="ew")

    tipo_pago = ctk.CTkOptionMenu(
        metodo_pago_frame,
        values=["", "CHEQUE", "TRANSF. ELECTRÓNICA"],
        font=FUENTE_TEXTO,
        dropdown_font=FUENTE_TEXTO,
        width=200,
        command=lambda _: mostrar_campos_pago()  
    )
    tipo_pago.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    tipo_pago.set("CHEQUE")  
    mostrar_campos_pago()     


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
        height=200,  # Aumentado para mejor visibilidad
        fg_color="transparent",
        scrollbar_fg_color=("#e5e7eb", "#374151"),
        scrollbar_button_color=("#9ca3af", "#4b5563"),
        scrollbar_button_hover_color=("#6b7280", "#374151"),
        corner_radius=8
    )
    filas_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=(0, 10))
    
    def configurar_scroll(widget):
        """Configura el scroll del widget"""
        def _on_mousewheel(event):
            if widget.winfo_exists():
                widget._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        widget.bind("<MouseWheel>", _on_mousewheel)
        widget.bind("<Button-4>", lambda e: widget._parent_canvas.yview_scroll(-1, "units"))
        widget.bind("<Button-5>", lambda e: widget._parent_canvas.yview_scroll(1, "units"))
    
    configurar_scroll(filas_frame)

    # Configuración de pesos
    conceptos_frame.grid_rowconfigure(2, weight=1)
    conceptos_frame.grid_columnconfigure(0, weight=2)  # Clave
    conceptos_frame.grid_columnconfigure(1, weight=4)  # Descripción
    conceptos_frame.grid_columnconfigure(2, weight=2)  # Importe
    conceptos_frame.grid_columnconfigure(3, weight=0)  # Botones

    entradas = []      
        
    
    
    def agregar_fila(enfocar_nueva_clave=False):
        fila_idx = len(entradas)
        
        fila_frame = ctk.CTkFrame(
            filas_frame, 
            fg_color=("#ffffff", "#1c1c1c"),
            border_width=1,
            #border_color=("#e5e7eb", "#374151"),
            corner_radius=6
            )
        fila_frame.pack(fill="x", pady=2, padx=2)     
        
         # Efecto hover
        def on_enter(e):
            fila_frame.configure(fg_color=("#f3f4f6", "#262626"))
        def on_leave(e):
            fila_frame.configure(fg_color=("#ffffff", "#1c1c1c"))
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
        entrada_importe.grid(row=0, column=2, padx=5, pady=2, sticky="ew")
        vcmd = fila_frame.register(solo_numeros_decimales)
        entrada_importe.configure(validate="key", validatecommand=(vcmd, "%P"))
        
        lista_sugerencias = configurar_lista_sugerencias(
        entrada_desc,
        entrada_clave,
        conceptos_frame,
        entradas,
        mostrar_sugerencias,
        ESTILO_LIST_SUG)
        
        entrada_importe.bind("<KeyRelease>", lambda event: actualizar_total(entradas, total, cargo_entry, validacion_totales, total, total_ctk))
        entrada_clave.bind("<FocusOut>", lambda event: llenar_por_clave(event, entrada_clave, entrada_desc))
        entrada_clave.bind("<Return>", lambda event: entrada_importe.focus_set())
        entrada_importe.bind("<Return>", lambda event: agregar_fila(enfocar_nueva_clave=True))
        entrada_desc.bind("<Return>", lambda e: seleccionar_sugerencia(e, entrada_clave, entrada_desc, lista_sugerencias, entradas))
        
        # Botón eliminar
        btn_eliminar = ctk.CTkButton(
            fila_frame,
            text="✕",
            width=30,
            height=30,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=lambda: (fila_frame.destroy(), entradas.remove((entrada_clave, entrada_desc, entrada_importe)), actualizar_total(entradas, total, cargo_entry, validacion_totales, total, total_ctk))
        )
        btn_eliminar.grid(row=0, column=3, padx=5, pady=2)

        # Configurar eventos
        entrada_clave.bind("<FocusOut>", lambda event: llenar_denominacion(event, entrada_clave, entrada_desc))
        entrada_clave.bind("<Return>", lambda event: entrada_importe.focus_set())

        entradas.append((entrada_clave, entrada_desc, entrada_importe))

        if enfocar_nueva_clave:
            entrada_clave.focus_set()

    # Agregar primera fila por defecto
    if not es_edicion:
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
        placeholder_text="Ingrese la denominacion...",
        #height=40,
        **ESTILO_ENTRADA
    )
    denominacion_entry.pack(fill="x", padx=10, pady=(0, 10))


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

    # Sección de observaciones
    observaciones_frame = ctk.CTkFrame(contenedor_principal, **ESTILO_FRAME)
    observaciones_frame.pack(fill="x", pady=(0, 20), padx=5)

    ctk.CTkLabel(
        observaciones_frame,
        text="OBSERVACIONES",
        font=FUENTE_SUBTITULO
    ).pack(pady=(5, 10))

    observaciones_textbox = ctk.CTkTextbox(
        observaciones_frame,
        **ESTILO_ENTRADA_TEXTBOX
    )
    observaciones_textbox.pack(fill="both", padx=10, pady=(0, 10), expand=True)


#----------------------------------- Barra de acciones inferiores---------------------------------------------------------
   
    acciones_frame = ctk.CTkFrame(
        frame_padre, 
        fg_color="transparent",
        corner_radius=16,    
        #border_width=2,     
        #border_color="#3b82f6"
        )
    acciones_frame.pack(fill="x", pady=(0, 15), padx=20)
    
    # Configura columnas para que crezcan
    acciones_frame.grid_columnconfigure(0, weight=0)  # Label Total
    acciones_frame.grid_columnconfigure(1, weight=0)  # Entry Total
    acciones_frame.grid_columnconfigure(2, weight=0)  # Validación
    acciones_frame.grid_columnconfigure(3, weight=1)  # Espacio flexible
    acciones_frame.grid_columnconfigure(4, weight=0)  # Guardar
    acciones_frame.grid_columnconfigure(5, weight=0)  # Descargar
    acciones_frame.grid_columnconfigure(6, weight=0)  # Buscar

    # Total y validación
    total_ctk = ctk.CTkLabel(
        acciones_frame,
        text="Total:",
        font=FUENTE_LABEL        
    )
    total_ctk.grid(row=0, column=0, sticky="w", padx=(0, 5))

    total = ctk.CTkEntry(
        acciones_frame,
        width=150,
        state="readonly",
        font=FUENTE_TEXTO,
        justify="right"
    )
    total.grid(row=0, column=1, sticky="w", padx=(0, 5))

    validacion_totales = ctk.CTkLabel(
        acciones_frame,
        text="?",
        font=("Arial", 16, "bold"),
        text_color="#6b7280"
    )
    validacion_totales.grid(row=0, column=2, sticky="w", padx=(0, 5))
    
    def guardar_poliza():
        try:
            poliza = capturar_poliza(form, entradas)
            if poliza is None:
                messagebox.showerror("Error", "No se pudo capturar la información.")
                return False

            if es_edicion:
                exito = actualizar_poliza(poliza)
                mensaje = "Póliza actualizada correctamente" if exito else "No se pudo actualizar la póliza."
            else:
                exito, mensaje = inrtar_poliza_egreso(poliza)

            if exito:
                if es_edicion:
                    from ui.detalle_egresos import mostrar_detalles_egresos
                    mostrar_detalles_egresos(frame_padre)
                return True
            else:
                messagebox.showerror("Error", mensaje)
                return False
        except Exception as e:
            print("Error en guardar_poliza:", e)
            messagebox.showerror("Error", f"Ocurrió un error al guardar:\n{e}")
            return False


    # Botones de acción
    btn_guardar = ctk.CTkButton(
        acciones_frame,
        text="💾 Actualizar" if es_edicion else "💾 Guardar",
        width=50,
        **ESTILO_BOTON,
        fg_color="#10b981",
        hover_color="#059669"
    )
    btn_guardar.grid(row=0, column=4, padx=5, sticky="e")
    
    btn_guardar.configure(command=lambda: ejecutar_con_loading(
        guardar_poliza,
        btn_guardar,
        btn_descargar,
        contenedor_principal,
        lambda: limpiar_formulario(contenedor_principal, mostrar_formulario_egresos, frame_padre),
        es_edicion
    ))

    btn_descargar = ctk.CTkButton(
        acciones_frame,
        text="📥 Descargar",
        width=50,
        **ESTILO_BOTON,
        fg_color="#3b82f6",
        hover_color="#2563eb",
        command=lambda: mostrar_menu_descarga(form, entradas)
    )
    btn_descargar.grid(row=0, column=5, padx=5, sticky="e")

    abrir_carp = ctk.CTkButton(
        acciones_frame,
        text=" Abrir Carpeta",
        width=50,
        **ESTILO_BOTON,
        fg_color="#6b7280",
        hover_color="#4b5563",
        command=lambda: abrir_carpeta(config["carpeta_destino"],"PolizasDeEgresos")
    )
    abrir_carp.grid(row=0, column=6, padx=5, sticky="e")

    if es_edicion:
        entrada_id.insert(0, poliza_editar.poliza_id)
        
    # Obtener número y sufijo por separado
    def mostrar_menu_descarga(form, entradas):
        menu = tk.Menu(None, tearoff=0)
        poliza = capturar_poliza(form, entradas)
        #print("Poliza capturada:", poliza)
        if not poliza:
            messagebox.showerror("Error", "No se pudo capturar la información de la póliza.")
            return
        # usar `poliza` directamente después

        menu.add_command(
            label="Exportar como PDF",
            command=lambda: ejecutar_con_loading(
                guardar_pdf,
                btn_guardar,
                btn_descargar,
                contenedor_principal,
                lambda: limpiar_formulario(contenedor_principal, mostrar_formulario_egresos, frame_padre),
                es_edicion,
                poliza,
                
                
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
                es_edicion,
                poliza,
            )
        )
        try:
            x = btn_descargar.winfo_rootx()
            y = btn_descargar.winfo_rooty() + btn_descargar.winfo_height()
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()
            
    def mostar_menu_op(): 
        menu = tk.Menu(None, tearoff=0)
        menu.add_command(
            label = "Generar libro del mes",
            command = lambda: confirmar_y_generar()
        )
        try:
            x= btn_guardar.winfo_rootx()
            y = btn_guardar.winfo_rooty() + btn_guardar.winfo_height()
            menu.tk_popup(x, y)
        finally:
            menu.grab_release()
            
    btn_iopciones = ctk.CTkButton(
        acciones_frame,
        text="⋮ Opciones",
        width = 50,
        fg_color= "transparent",
        hover_color="#4b5563",
        command=mostar_menu_op
    )        
    btn_iopciones.grid(row=0, column=3, padx=5, sticky="e")
    

    form = {
        "poliza_id": entrada_id,
        "numero": no_poliza,
        "sufijo": sufijo_fecha,
        "fecha": fecha_policia,
        "nombre": nombre,
        "cargo": cargo_entry,
        "monto_letra": cargo_letras_entry,
        "tipo_pago": tipo_pago,
        "clave_rastreo": clave_rastreo,
        "observaciones": observaciones_textbox,
        "denominacion": denominacion_entry,
        "no_cheque": no_cheque_entry,  
    }
    
    if es_edicion:
        if "/" in poliza_editar.no_poliza:
            numero, sufijo = poliza_editar.no_poliza.split("/", 1)
            sufijo = "/" + sufijo
        else:
            numero = poliza_editar.no_poliza
            sufijo = ""

        no_poliza.insert(0, numero)
        sufijo_fecha.configure(state="normal")
        sufijo_fecha.insert(0, sufijo)
        sufijo_fecha.configure(state="readonly")
        fecha_policia.set_date(poliza_editar.fecha)
        nombre.insert(0, poliza_editar.nombre)
        cargo_entry.insert(0, poliza_editar.monto)
        tipo_pago.set(poliza_editar.tipo_pago)
        actualizar_cargo_letras()
        clave_rastreo.insert(0, poliza_editar.clave_ref or "")
        mostrar_campos_pago() 
        observaciones_textbox.insert("1.0", poliza_editar.observaciones)
        denominacion_entry.insert(0, poliza_editar.denominacion or "")
        no_cheque_entry.insert(0, poliza_editar.no_cheque or "")
        for concepto in poliza_editar.conceptos:
            agregar_fila()
            entrada_clave, entrada_desc, entrada_importe = entradas[-1]
            entrada_clave.insert(0, concepto.clave_cucop)
            entrada_desc.configure(state="normal")
            entrada_desc.insert(0, concepto.descripcion)
            entrada_desc.configure(state="readonly")
            entrada_importe.insert(0, concepto.cargo)
            
    actualizar_total(entradas, total, cargo_entry, validacion_totales, total, total_ctk)    