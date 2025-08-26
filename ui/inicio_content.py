import customtkinter as ctk
import tkinter as tk
from functions.genRegIngresos import confirmar_y_generar
from informes.Auxi_acre_div import confirmar_y_generar_Auxiliar_acree
from informes.aux_bancario import confirmar_y_generar_aux_bancario
from informes.aux_deudores_div import confirmar_y_generar_aux_deudor
from informes.consolidado_egre import confirmar_y_generar_consolidado
from informes.inf_real_egre import confirmar_y_generar_infReal
from informes.lib_regis_egresos import confirmar_y_generar_egresos
from informes.inf_real_ingresos import confirmar_y_generar_inf_real_ingresos
#from ui.formIngresosDiarios import mostrar_formulario_ingresos
from styles.styles import *
from PIL import Image
from customtkinter import CTkImage
import datetime
from functions.funcions import confirmar_aux, confirmar_y_generar2
import os
from utils.rutas import ruta_absoluta
from utils.rutas import ruta_absoluta
from utils.utils import abrir_carpeta
from utils.config_utils import cargar_config
from functions.genObservaciones import seleccionar_poliza

config = cargar_config()

def mostrar_inicio(contenedor):
    app = ctk.CTk()  # o CTkFrame si estás usando frames
    app.withdraw()   
    # Frame interno para mejor organización
    main_frame = ctk.CTkScrollableFrame(
        master=contenedor,
        fg_color="transparent",
        scrollbar_button_color="#4b5563",  # opcional, puedes personalizar colores
        scrollbar_button_hover_color="#6b7280"
    )
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Encabezado con sombra y mejor jerarquía visual
    header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 20))

    # Título con efecto de gradiente de color
    titulo = ctk.CTkLabel(
        header_frame, 
        text="Sistema de Gestión CECATI 122",
        font=("Arial", 24, "bold"),
        text_color=TEXT_PRIMARY
    )
    titulo.pack(pady=(10, 5))

    # Subtítulo con estilo moderno
    subtitulo = ctk.CTkLabel(
        header_frame, 
        text="Panel principal del sistema administrativo",
        font=("Arial", 14),
        text_color=("#6b7280", "#9ca3af")
    )
    subtitulo.pack()

    # Separador decorativo
    separador = ctk.CTkFrame(
        header_frame, 
        height=2, 
        fg_color=("#d1d5db", "#4b5563"), 
        width=150
    )
    separador.pack(pady=10)

    # Sección superior con información útil
    top_info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    top_info_frame.pack(fill="x", pady=(0, 20))

    # Widget de fecha y hora actual
    datetime_frame = ctk.CTkFrame(top_info_frame, fg_color=("#f3f4f6", "#1f2937"), corner_radius=10)
    datetime_frame.pack(side="left", padx=10)
    
    # Contenedor horizontal para fecha + botón
    fecha_container = ctk.CTkFrame(datetime_frame, fg_color="transparent")
    fecha_container.pack(pady=(8, 0), padx=8, fill="x")

    fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

    fecha_label = ctk.CTkLabel(
        datetime_frame,
        text=fecha_actual,
        font=("Arial", 14, "bold"),
        text_color=("#111827", "#f9fafb")
    )
    fecha_label.pack(pady=(10, 0), padx=15)
    
    calendar_path = ruta_absoluta(os.path.join("assets", "calendar1.png"))
    try:
        # Verificar si la imagen existe
        if os.path.exists(calendar_path):
            calendar_icon = ctk.CTkImage(
                light_image=Image.open(calendar_path),
                dark_image=Image.open(calendar_path),
                size=(28, 28)  # Tamaño ligeramente menor para mejor proporción
            )
        else:
            raise FileNotFoundError
    except Exception as e:
        print(f"[Error] No se pudo cargar el icono: {str(e)}")
        # Fallback visual elegante
        calendar_icon = None
        calendar_text = "📅"
    else:
        calendar_text = ""  # Mostrar solo imagen
    # 2. Botón de calendario (icono)
    calendario_btn = ctk.CTkButton(
        fecha_container,
        text=calendar_text,  # Solo muestra el emoji si no hay imagen
        image=calendar_icon, # Alternativa: usar CTkImage con icono personalizado
        width=30,
        height=30,
        corner_radius=8,
        fg_color="transparent",
        hover_color=("#d1d5db", "#4b5563"),
        command=lambda: mostrar_calendario(fecha_label)  # Función al hacer clic
    )
    calendario_btn.pack(side="right")
    
    # --- Función para mostrar calendario ---
    def mostrar_calendario(label_fecha):
        popup = ctk.CTkToplevel()
        popup.title("Calendario")
        popup.geometry("300x300")
        popup.grab_set()  # Ventana modal
    
        # Calendario (requiere tkcalendar: pip install tkcalendar)
        from tkcalendar import Calendar
        cal = Calendar(
            popup, 
            selectmode="day",
            date_pattern="dd/mm/yyyy",
            locale="es",
            font=("Helvetica", 16),
            background="#f3f4f6" if ctk.get_appearance_mode() == "Light" else "#1f2937",
            foreground="black" if ctk.get_appearance_mode() == "Light" else "white"
        )
        cal.pack(pady=20, fill="both", expand=True)
    
    # --------------------------------------------------------------------------------------

    def crear_tarjeta_moderna_con_menu(parent, nombre, icono, color, opciones, boton_texto="Opciones", command=None):
        tarjeta = ctk.CTkFrame(
            parent,
            fg_color=color[0],
            corner_radius=20,
            border_width=0,
            width=240,
            height=180,
        )

        icono_frame = ctk.CTkFrame(
            tarjeta,
            width=48,
            height=48,
            corner_radius=10,
            fg_color="transparent",
            #fg_color=("#ffffff", "#18181b"),
            #border_radius=2
        )
        icono_frame.pack(pady=(15, 10))

        try:
            icon_img = ctk.CTkImage(Image.open(icono), size=(64, 64))
            ctk.CTkLabel(icono_frame, image=icon_img, text="").place(relx=0.5, rely=0.5, anchor="center")
        except:
            ctk.CTkLabel(icono_frame, text="📊", font=("Arial", 20)).place(relx=0.5, rely=0.5, anchor="center")

        titulo = ctk.CTkLabel(
            tarjeta,
            text=nombre,
            font=("Segoe UI", 14, "bold"),
            text_color="#ffffff",
            wraplength=160,
            justify="center"
        )
        titulo.pack(pady=(0, 8))

        if not opciones:
            opciones = ["Próximamente"]

        menu = ctk.CTkOptionMenu(
            tarjeta,
            values=opciones,
            fg_color=color[1],
            button_color=color[0],
            dropdown_fg_color="#2a2d32",
            dropdown_text_color="#ffffff",
            font=("Segoe UI", 12),
            width=140,
            command=command
        )
        menu.set(boton_texto)
        menu.pack(pady=(0, 10))

        def on_enter(e):
            tarjeta.configure(fg_color=color[1])

        def on_leave(e):
            tarjeta.configure(fg_color=color[0])

        tarjeta.bind("<Enter>", on_enter)
        tarjeta.bind("<Leave>", on_leave)
        return tarjeta
    
    def crear_menu_command(comandos, nombre_local):
        def menu_command(opcion):
            if comandos and opcion in comandos and callable(comandos[opcion]):
                comandos[opcion]()
            else:
                print(f"{nombre_local}: {opcion}")
        return menu_command


    
    egresos_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    egresos_frame.pack(fill="x", pady= 10)
    
    titulo_egresos_ingresos = ctk.CTkLabel(
        egresos_frame,
        text="Egresos",
        font=("Arial", 18, "bold"),
        text_color=("#2a2d32", "#ffffff"),
        anchor="w",
    )
    titulo_egresos_ingresos.pack(anchor="w", padx=10, pady=(0, 10))

    tarjetas_egresos = ctk.CTkFrame(egresos_frame, fg_color="transparent")
    tarjetas_egresos.pack(fill="x", padx=10)

    tarjetas_ei_info = [
        (
            "Libro de Egresos", 
         "assets/wallet.png", 
         (
             "#ef4444", 
             "#dc2626"), 
         [
             "Generar",
             "Abrir Carpeta"], 
         "Opciones", 
         {
             "Generar": lambda:confirmar_y_generar_egresos(contenedor_principal=contenedor),
             "Abrir Carpeta": lambda: abrir_carpeta(config["carpeta_destino"], "Libro de Egresos")}),
        
        (
            "Inf. Consolidado de egresos", "assets/excel2.png", 
            ("#ef4444", 
             "#dc2626"), 
            [
                "Generar",
                "Abrir Carpeta"],
            "Opciones", 
            {
                "Generar": lambda: confirmar_y_generar_consolidado(contenedor_principal=contenedor),
                "Abrir Carpeta": lambda: abrir_carpeta(config["carpeta_destino"], "Consolidado de egresos")}),
        
        ("Inf. Real de egresos", 
         "assets/excel2.png", 
         ("#ef4444", "#dc2626"), 
         [
             "Generar",
             "Abrir Carpeta"], 
         "Opciones", 
         {
             "Generar": lambda: confirmar_y_generar_infReal(contenedor_principal = contenedor),
             "Abrir Carpeta": lambda: abrir_carpeta(config["carpeta_destino"], "Informe Real Egresos")}),
        
        ("Notas en COMPERCO y OCOMI", 
         "assets/excel2.png", 
         (
             "#ef4444", 
             "#dc2626"), 
         ["Insertar"], "Opciones", {"Insertar": seleccionar_poliza})
    ]

    columnas = 4
    
    for col in range(columnas):
            tarjetas_egresos.grid_columnconfigure(col, weight=1)
            
    for idx, (nombre, icono, color, opciones, boton_texto, comandos) in enumerate(tarjetas_ei_info):
        fila = idx // columnas
        columna = idx % columnas

        menu_command = crear_menu_command(comandos, nombre)

        tarjeta = crear_tarjeta_moderna_con_menu(
            parent=tarjetas_egresos,
            nombre=nombre,
            icono=ruta_absoluta(icono),
            color=color,
            opciones=opciones,
            boton_texto=boton_texto,
            command=menu_command
        )
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")
 
 
 
    ingresos_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    ingresos_frame.pack(fill="x", pady= 10)
    
    titulo_ingresos = ctk.CTkLabel(
        ingresos_frame,
        text="Ingresos",
        font=("Arial", 18, "bold"),
        text_color=("#2a2d32", "#ffffff"),
        anchor="w",
    )
    titulo_ingresos.pack(anchor="w", padx=10, pady=(0, 10))
        
    # Sección de tarjetas con diseño más profesional
    tarjetas_ingresos = ctk.CTkFrame(ingresos_frame, fg_color="transparent")
    tarjetas_ingresos.pack(fill="x", pady=20)

    tarjetas_info = [
        ("Libro de Ingresos", "assets/coin.png", ("#10b981", "#059669"), ["Libro de Ingresos"], "Opciones", {"Libro de Ingresos":confirmar_y_generar}),
        ("Inf. Consolidado de Ingresos", "assets/excel2.png", ("#10b981", "#059669"), ["Generar"], "Opciones", {"Generar": confirmar_y_generar2}),
        ("Inf. Real de Ingresos", "assets/excel2.png", ("#10b981", "#059669"), ["Generar"], "Opciones", {"Generar": lambda: confirmar_y_generar_inf_real_ingresos(contenedor_principal = contenedor)})
    ]
    
    columnas = 4
    
    for col in range(columnas):
            tarjetas_ingresos.grid_columnconfigure(col, weight=1)
            
    for idx, (nombre, icono, color, opciones, boton_texto, comandos) in enumerate(tarjetas_info):
        fila = idx // columnas
        columna = idx % columnas

        def menu_command(opcion, cmd=comandos, nombre_local=nombre):
            if cmd and opcion in cmd and callable(cmd[opcion]):
                cmd[opcion]()
            else:
                print(f"{nombre_local}: {opcion}")

        tarjeta = crear_tarjeta_moderna_con_menu(
            parent=tarjetas_ingresos,
            nombre=nombre,
            icono=ruta_absoluta(icono),
            color=color,
            opciones=opciones,
            boton_texto=boton_texto,
            command=menu_command
        )
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")
        
        
    
    auxil_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    auxil_frame.pack(fill="x", pady= 10)
    
    titulo_auxil = ctk.CTkLabel(
        auxil_frame,
        text="Auxiliares",
        font=("Arial", 18, "bold"),
        text_color=("#2a2d32", "#ffffff"),
        anchor="w",
    )
    titulo_auxil.pack(anchor="w", padx=10, pady=(0, 10))
        
    # Sección de tarjetas con diseño más profesional
    tarjetas_auxil = ctk.CTkFrame(auxil_frame, fg_color="transparent")
    tarjetas_auxil.pack(fill="x", pady=20)

    tarjetas_info = [
        (
            "Aux. Bancario", 
            "assets/coin.png", 
            ("#f59e0b", "#d97706"), 
            [
                "Generar",
                "Abrir Carpeta"], 
            "Opciones", 
            {"Generar": confirmar_y_generar_aux_bancario,
             "Abrir Carpeta": lambda: abrir_carpeta(config["carpeta_destino"], "Auxiliar Bancario")}),
        
        
        (
            "Aux. Acreedores diversos", 
            "assets/excel2.png", 
            ("#f59e0b", "#d97706"), 
            [
                "Generar",
                "Abrir Carpeta"], 
            "Opciones", 
            {
                "Generar": confirmar_y_generar_Auxiliar_acree,
                "Abrir Carpeta": lambda: abrir_carpeta(config["carpeta_destino"], "Auxiliar Acreedores diversos")}),
        
        (
            "Aux. deudores diversos", 
            "assets/coin.png", 
            ("#f59e0b", "#d97706"), 
            [
                "Generar",
                "Abrir Carpeta"], 
            "Opciones", 
            {
                "Generar": confirmar_y_generar_aux_deudor,
                "Abrir Carpeta": lambda: abrir_carpeta(config["carpeta_destino"], "Auxiliar Deudores Diversos")}),
    ]
    
    columnas = 4
    
    for col in range(columnas):
            tarjetas_auxil.grid_columnconfigure(col, weight=1)
            
    for idx, (nombre, icono, color, opciones, boton_texto, comandos) in enumerate(tarjetas_info):
        fila = idx // columnas
        columna = idx % columnas

        def menu_command(opcion, cmd=comandos, nombre_local=nombre):
            if cmd and opcion in cmd and callable(cmd[opcion]):
                cmd[opcion]()
            else:
                print(f"{nombre_local}: {opcion}")

        tarjeta = crear_tarjeta_moderna_con_menu(
            parent=tarjetas_auxil,
            nombre=nombre,
            icono=ruta_absoluta(icono),
            color=color,
            opciones=opciones,
            boton_texto=boton_texto,
            command=menu_command
        )
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")        
        
        
        
      
#-------------------------
    
   
    # boton para abrir la carpeta de informes
    acciones_frame = ctk.CTkFrame(
        contenedor,
        fg_color="transparent",
        corner_radius=12,
        )
    acciones_frame.pack(fill="x", padx=20, pady=(0, 10))
    
    abrir_carpeta_archivos = ctk.CTkButton(
        acciones_frame,
        width=50,
        text="Abrir carpeta",
        command=lambda: abrir_carpeta(config["carpeta_destino"], ""),
        image=CTkImage(Image.open(ruta_absoluta("assets/icons/file.png")), size=(28, 28)),
        **ESTILO_BOTON,
        
    )
    abrir_carpeta_archivos.pack(padx=20, fill="x", side="right")
