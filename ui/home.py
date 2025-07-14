import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from styles.styles import *
from ui.detalle_egresos import mostrar_detalles_egresos
from ui.inicio_content import mostrar_inicio
from ui.egresos import mostrar_formulario_egresos
from ui.formIngresosDiarios import mostrar_formulario_ingresos
from ui.ajustes import mostrar_ajustes
from ui.detalleIngresos import mostrar_detalles_ingresos, estilo_tabla
from PIL import Image, ImageTk
from customtkinter import CTkImage, CTkFont
import json
from utils.config_utils import actualizar_config
from utils.rutas import ruta_absoluta

CONFIG_PATH = ruta_absoluta("config.json")
from utils.config_utils import cargar_config

vista_act = None

def guardar_estado_ventana(root):
    actualizar_config("geometry", root.geometry())
    actualizar_config("state", root.state())
    actualizar_config("appearance_mode", ctk.get_appearance_mode())
    actualizar_config("appearance_mode", ctk.get_appearance_mode())
    actualizar_config("color_theme", "blue")  
    
def cargar_estado_ventana(root):
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                config = json.load(f)
            if "geometry" in config:
                root.geometry(config["geometry"])
            if "state" in config and config["state"] not in ("normal", "zoomed"):
                root.state(config["state"])
        except Exception:
            pass
        
config = cargar_config()
ctk.set_appearance_mode(config.get("appearance_mode", "dark"))
ctk.set_default_color_theme(config.get("color_theme", "blue"))        
        
def lanzar_ventana_principal():
    root = ctk.CTk()
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Seguro que deseas cerrar el programa?"):
            root.destroy()

    
    root.iconbitmap(ruta_absoluta("assets/cecati-122.ico"))
    root.title("Sistema de Gestión CECATI 122")
    
    # ---------------- HEADER ----------------
    header = ctk.CTkFrame(
        root, 
        height=70, 
        fg_color= COLOR_CONT_PRIMARIO, 
    )
    header.pack(fill="x", pady=(0, 2))   
    
    # Espaci y usuario
    header_space = ctk.CTkLabel(header, text="")
    header_space.pack(side="left", expand=True, fill="x")
    
    user_info = ctk.CTkLabel(
        header, 
        text="Usuario: Admin", 
        font=CTkFont("Arial", 12),
        text_color=COLOR_TEXTO_SEMIVISIBLE
    )
    user_info.pack(side="right", padx=20)

    # ---------------- MAIN CONTAINER CON DISEÑO MODERNO ----------------
    main_container = ctk.CTkFrame(root, fg_color="transparent")
    main_container.pack(fill="both", expand=True)

    # Configuración responsiva mejorada
    main_container.grid_rowconfigure(0, weight=1)
    main_container.grid_columnconfigure(0, weight=0, minsize=240)  # Sidebar más ancho
    main_container.grid_columnconfigure(1, weight=1)  # Content área principal

    # Colores y botones
    sidebar_buttons = []

    def cambiar_boton_activo(boton_activo):
        for btn in sidebar_buttons:
            if btn == boton_activo:
                btn.configure(
                    fg_color=COLOR_ACTIVO,
                    text_color=("#ffffff", "#ffffff"),
                    hover_color=("#2563eb", "#1d4ed8")
                )
            else:
                btn.configure(
                    fg_color=COLOR_INACTIVO,
                    text_color=("#f8fafc", "#f1f5f9"),
                    hover_color=("#334155", "#475569")
                )

    def create_sidebar_btn(parent, text, image_path, command):
        image = CTkImage(Image.open(image_path), size=(24, 24))
        def wrapped_command():
            cambiar_boton_activo(btn)
            command()
        btn = ctk.CTkButton(
            parent, 
            text=text, 
            image=image, 
            command=wrapped_command,
            anchor="w",
            font=CTkFont("Arial", 14),
            corner_radius=8,
            height=40,
            fg_color=COLOR_INACTIVO,
            text_color=COLOR_TEXTO,
            hover_color= COLOR_PRIMARIO
        )
        btn.pack(fill="x", padx=12, pady=4)
        return btn

    # ---------------- SIDEBAR MODERNO ----------------
    sidebar = ctk.CTkFrame(
        main_container, 
        width=240, 
        fg_color=COLOR_CONT_PRIMARIO, 
       
    )
    sidebar.grid(row=0, column=0, sticky="nsew")

    # Logo en sidebar
    sidebar_logo = ctk.CTkLabel(
        sidebar, 
        text="", 
        image=CTkImage(Image.open(ruta_absoluta("assets/cecati-122.ico"))),
    )
    sidebar_logo.pack(pady=(20, 10))

    sidebar_title = ctk.CTkLabel(
        sidebar, 
        text="MENÚ PRINCIPAL", 
        font=CTkFont("Arial", 12, "bold"), 
        text_color=COLOR_TEXTO_SEMIVISIBLE
    )
    sidebar_title.pack(pady=(0, 10))
    
    separator = ctk.CTkFrame(
        sidebar, 
        height=1, 
        fg_color=COLOR_TEXTO_APARTADO
    )
    separator.pack(fill="x", pady=5, padx=15)

    # ---------------- CONTENIDO PRINCIPAL ----------------
    content_frame = ctk.CTkFrame(
        main_container, 
        fg_color=COLOR_CONT_SECUNDARIO
    )
    content_frame.grid(row=0, column=1, sticky="nsew")

    # ÁREA DE CONTENIDO DINÁMICO CON SOMBRA
    frame_contenido = ctk.CTkFrame(
        content_frame, 
       
        fg_color=COLOR_CONT_PRIMARIO,
    )
    frame_contenido.pack(fill="both", expand=True, padx=20, pady=20)

    # Funciones para cambiar contenido
    def abrir_formulario(contenedor):
        limpiar_contenido(contenedor)
        mostrar_formulario_ingresos(contenedor)

    def abrir_inicio(contenedor):
        limpiar_contenido(contenedor)
        mostrar_inicio(contenedor)

    def abrir_formulario_egresos(contenedor):
        limpiar_contenido(contenedor)
        mostrar_formulario_egresos(contenedor)
        
    def abrir_det_Egresos(contenedor):
        limpiar_contenido(contenedor)
        mostrar_detalles_egresos(contenedor)
        
    def abrir_det_ingresos(contenedor):
        limpiar_contenido(contenedor)
        from ui.detalleIngresos import mostrar_detalles_ingresos
        mostrar_detalles_ingresos(contenedor)
        registrar_vista(mostrar_detalles_ingresos, contenedor)  # ¡Registra la vista!

    def abrir_ajustes(contenedor):
        limpiar_contenido(contenedor)
        mostrar_ajustes(contenedor)

    def limpiar_contenido(contenedor):
        for widget in contenedor.winfo_children():
            widget.destroy()
        contenedor.update_idletasks()

    # ---------------- BOTONES DEL SIDEBAR MEJORADOS ----------------
    btn_inicio_sidebar = create_sidebar_btn(
        sidebar, 
        "Inicio", 
        ruta_absoluta("assets/house.png"), 
        lambda: abrir_inicio(frame_contenido)
    )
    
    # Sección Pólizas
    ctk.CTkLabel(
        sidebar, 
        text="PÓLIZAS", 
        font=CTkFont("Arial", 11, "bold"), 
        text_color= COLOR_TEXTO_APARTADO_SECUNDARIO
    ).pack(pady=(15, 5), anchor="w", padx=20)
    
    separator = ctk.CTkFrame(
        sidebar, 
        height=1, 
        fg_color=("#334155", "#475569")
    )
    separator.pack(fill="x", pady=2, padx=15)
    
    btn_ingresos_sidebar = create_sidebar_btn(
        sidebar, 
        "Ingresos", 
        ruta_absoluta("assets/coin.png"),  
        lambda: abrir_formulario(frame_contenido)
    )
    btn_Egresos_sidebar = create_sidebar_btn(
        sidebar, 
        "Egresos", 
        ruta_absoluta("assets/wallet.png"),  
        lambda: abrir_formulario_egresos(frame_contenido)
    )
    
    
    separator = ctk.CTkFrame(
        sidebar, 
        height=1, 
        fg_color=COLOR_TEXTO_APARTADO
    )
    separator.pack(fill="x", pady=2, padx=15)
    
    # Sección Visualizacion
    ctk.CTkLabel(
        sidebar, 
        text="DETALLES", 
        font=CTkFont("Arial", 11, "bold"), 
        text_color= COLOR_TEXTO_APARTADO_SECUNDARIO
    ).pack(pady=(15, 5), anchor="w", padx=20)
    
    btn_detalles_ing = create_sidebar_btn(
        sidebar, 
        "Ver Ingresos", 
        ruta_absoluta("assets/lookup.png"),  
        lambda: abrir_det_ingresos(frame_contenido)
    )
    
    btn_detalles_egre = create_sidebar_btn(
        sidebar,
        "Ver Egresos",
        ruta_absoluta("assets/lookup.png"),
        lambda:abrir_det_Egresos(frame_contenido)
    )

    # Espacio flexible antes de los botones inferiores
    spacer = ctk.CTkLabel(sidebar, text="")
    spacer.pack(fill="y", expand=True)

    # Botones inferiores
    btn_config = create_sidebar_btn(
        sidebar, 
        "Ajustes", 
        ruta_absoluta("assets/settings 2.png"),
        lambda: abrir_ajustes(frame_contenido)
    )
    
    vista_actual = None
    contenedor_actual = None
    
    def registrar_vista(funcion, contenedor):
        global vista_actual, contenedor_actual
        vista_actual = funcion
        contenedor_actual = contenedor
        
    def refrescar_vista_actual():
        if vista_actual and contenedor_actual:
            limpiar_contenido(contenedor_actual)
            vista_actual(contenedor_actual)
    
    # Botón de tema con mejor diseño
    def cambiar_tema():
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("light")
            imagenes["tema"] = CTkImage(Image.open(ruta_absoluta("assets/sun 2.png")), size=(20, 20))
            btn_tema.configure(text="Modo Claro", image=imagenes["tema"])
            actualizar_config("appearance_mode", "light")
        else:
            ctk.set_appearance_mode("dark")
            imagenes["tema"] = CTkImage(Image.open(ruta_absoluta("assets/moon 2.png")), size=(20, 20))
            btn_tema.configure(text="Modo Oscuro", image=imagenes["tema"])
            actualizar_config("appearance_mode", "dark")
          
        if contenedor_actual:  
            refrescar_vista_actual()

    imagenes = {
    "tema": CTkImage(Image.open(ruta_absoluta("assets/moon 2.png")), size=(20, 20))
    }
    
    btn_tema = ctk.CTkButton(
        sidebar,
        text="Modo Oscuro",
        command=cambiar_tema,
        image=imagenes["tema"],
        anchor="w",
        font=CTkFont("Arial", 14),
        corner_radius=8,
        height=40,
        fg_color=COLOR_INACTIVO,
        text_color=("#121212", "#f1f5f9"),
        hover_color=("#d21329", "#d21329")
    )
    btn_tema.pack(fill="x", padx=12, pady=(10, 5))

    btn_salir_sidebar = create_sidebar_btn(
        sidebar, 
        "Salir", 
        ruta_absoluta("assets/output.png"),
        lambda: (guardar_estado_ventana(root), root.destroy())
    )
    
    # Cargar pantalla inicial
    abrir_inicio(frame_contenido)
    cambiar_boton_activo(btn_inicio_sidebar)
    
    root.after(0, lambda: cargar_estado_ventana(root))
    root.protocol("WM_DELETE_WINDOW", lambda: (guardar_estado_ventana(root), root.destroy()))
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()