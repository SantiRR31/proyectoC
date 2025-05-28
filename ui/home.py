import tkinter as tk
import customtkinter as ctk
from styles.styles import *
from ui.inicio_content import mostrar_inicio
from ui.egresos import mostrar_formulario_egresos
from ui.formIngresosDiarios import mostrar_formulario_ingresos
from ui.infRealIngresos import mostrar_informe_real_ingresos
from ui.ajustes import mostrar_ajustes
from PIL import Image, ImageTk
from customtkinter import CTkImage, CTkFont


def lanzar_ventana_principal():
    # Configuración inicial con tema moderno
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.iconbitmap("assets/cecati-122.ico")
    root.title("Sistema de Gestión CECATI 122")
    #root.geometry("1280x720")
    #root.minsize(1024, 720)
    
    
    clave_cecati = tk.StringVar(value="22DBT0005P")

    # ---------------- HEADER MODERNO ----------------
    header = ctk.CTkFrame(
        root, 
        height=70, 
        fg_color=("#faf7f6", "#191919"), 
    )
    header.pack(fill="x", pady=(0, 2))  # Pequeño margen inferior
    
    
    
    # Espacio flexible y usuario
    header_space = ctk.CTkLabel(header, text="")
    header_space.pack(side="left", expand=True, fill="x")
    
    user_info = ctk.CTkLabel(
        header, 
        text="Usuario: Admin", 
        font=CTkFont("Arial", 12),
        text_color=("#94a3b8", "#cbd5e1")
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
            text_color=("#121212", "#f1f5f9"),
            hover_color=("#d21329", "#d21329")
        )
        btn.pack(fill="x", padx=12, pady=4)
        return btn

    # ---------------- SIDEBAR MODERNO ----------------
    sidebar = ctk.CTkFrame(
        main_container, 
        width=240, 
        fg_color=("#faf7f6", "#191919"), 
       
    )
    sidebar.grid(row=0, column=0, sticky="nsew")

    # Logo en sidebar
    sidebar_logo = ctk.CTkLabel(
        sidebar, 
        text="", 
        image=CTkImage(Image.open("assets/cecati-122.ico"), size=(40, 40))
    )
    sidebar_logo.pack(pady=(20, 10))

    sidebar_title = ctk.CTkLabel(
        sidebar, 
        text="MENÚ PRINCIPAL", 
        font=CTkFont("Arial", 12, "bold"), 
        text_color=("#94a3b8", "#cbd5e1")
    )
    sidebar_title.pack(pady=(0, 10))
    
    separator = ctk.CTkFrame(
        sidebar, 
        height=1, 
        fg_color=("#334155", "#475569")
    )
    separator.pack(fill="x", pady=5, padx=15)

    # ---------------- CONTENIDO PRINCIPAL ----------------
    content_frame = ctk.CTkFrame(
        main_container, 
        fg_color=("#ddd9d9", "#1c1c1c")
    )
    content_frame.grid(row=0, column=1, sticky="nsew")

    # ÁREA DE CONTENIDO DINÁMICO CON SOMBRA
    frame_contenido = ctk.CTkFrame(
        content_frame, 
       
        fg_color=("#faf7f6", "#191919"),
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
        
    def abrir_informe_real_ingresos(contenedor):
        limpiar_contenido(contenedor)
        mostrar_informe_real_ingresos(contenedor, clave_cecati)

    def abrir_ajustes(contenedor):
        limpiar_contenido(contenedor)
        mostrar_ajustes(contenedor, clave_cecati)

    def limpiar_contenido(contenedor):
        for widget in contenedor.winfo_children():
            widget.destroy()
        contenedor.update_idletasks()

    # ---------------- BOTONES DEL SIDEBAR MEJORADOS ----------------
    btn_inicio_sidebar = create_sidebar_btn(
        sidebar, 
        "Inicio", 
        "assets/house.png", 
        lambda: abrir_inicio(frame_contenido)
    )
    
    # Sección Pólizas
    ctk.CTkLabel(
        sidebar, 
        text="PÓLIZAS", 
        font=CTkFont("Arial", 11, "bold"), 
        text_color=("#64748b", "#94a3b8")
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
        "assets/coin.png", 
        lambda: abrir_formulario(frame_contenido)
    )
    btn_clientes_sidebar = create_sidebar_btn(
        sidebar, 
        "Egresos", 
        "assets/wallet.png", 
        lambda: abrir_formulario_egresos(frame_contenido)
    )
    
    # Sección Reportes
    ctk.CTkLabel(
        sidebar, 
        text="REPORTES", 
        font=CTkFont("Arial", 11, "bold"), 
        text_color=("#64748b", "#94a3b8")
    ).pack(pady=(15, 5), anchor="w", padx=20)
    
    separator = ctk.CTkFrame(
        sidebar, 
        height=1, 
        fg_color=("#334155", "#475569")
    )
    separator.pack(fill="x", pady=2, padx=15)
    
    btn_reportes_sidebar = create_sidebar_btn(
        sidebar, 
        "Reportes", 
        "assets/bar.png", 
        lambda: None
    )
    
    # Sección Informes
    ctk.CTkLabel(
        sidebar, 
        text="INFORMES", 
        font=CTkFont("Arial", 11, "bold"), 
        text_color=("#64748b", "#94a3b8")
    ).pack(pady=(15, 5), anchor="w", padx=20)
    
    separator = ctk.CTkFrame(
        sidebar, 
        height=1, 
        fg_color=("#334155", "#475569")
    )
    separator.pack(fill="x", pady=2, padx=15)
    
    btn_inf_real_sidebar = create_sidebar_btn(
        sidebar, 
        "Informe Real", 
        "assets/notepad.png", 
        lambda: abrir_informe_real_ingresos(frame_contenido)
    )

    # Espacio flexible antes de los botones inferiores
    spacer = ctk.CTkLabel(sidebar, text="")
    spacer.pack(fill="y", expand=True)

    # Botones inferiores
    btn_config = create_sidebar_btn(
        sidebar, 
        "Ajustes", 
        "assets/settings 2.png", 
        lambda: abrir_ajustes(frame_contenido)
    )
    
    # Botón de tema con mejor diseño
    def cambiar_tema():
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("light")
            imagenes["tema"] = CTkImage(Image.open("assets/sun 2.png"), size=(20, 20))
            btn_tema.configure(text="Modo Claro", image=imagenes["tema"])
        else:
            ctk.set_appearance_mode("dark")
            imagenes["tema"] = CTkImage(Image.open("assets/moon 2.png"), size=(20, 20))
            btn_tema.configure(text="Modo Oscuro", image=imagenes["tema"])

    imagenes = {
        "tema": CTkImage(Image.open("assets/moon 2.png"), size=(20, 20))
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
        "assets/output.png", 
        root.quit
    )

    # Cargar pantalla inicial
    abrir_inicio(frame_contenido)
    cambiar_boton_activo(btn_inicio_sidebar)

    root.mainloop()