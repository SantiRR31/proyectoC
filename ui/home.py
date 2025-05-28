import tkinter as tk
import customtkinter as ctk
from styles.styles import (
    btn_style,
    COLOR_FONDO,
    COLOR_ACTIVO,
    COLOR_INACTIVO,
    COLOR_SEPARADOR,
    FUENTE_TITULO,
    FUENTE_MENU,
    FUENTE_SUBMENU,
    COLOR_TEXTO
)
from ui.inicio_content import mostrar_inicio
from ui.egresos import mostrar_formulario_egresos
from ui.formIngresosDiarios import mostrar_formulario_ingresos
from ui.infRealIngresos import mostrar_informe_real_ingresos
from ui.ajustes import mostrar_ajustes
from PIL import Image
from customtkinter import CTkImage


def lanzar_ventana_principal():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.iconbitmap("assets/cecati-122.ico")
    root.title("Ventana Principal")
    root.geometry("1280x720")
    root.minsize(640, 720)
    root.configure(fg_color=COLOR_FONDO)
    
    clave_cecati = tk.StringVar(value="22DBT0005P")
    banco_caja = tk.StringVar(value="BANORTE")

    # ---------------- HEADER ----------------
    header = ctk.CTkFrame(root, height=60, fg_color=COLOR_FONDO, corner_radius=0)
    header.pack(fill="x")
    titulo = ctk.CTkLabel(header, text="Sistema de Gestión", font= FUENTE_TITULO , text_color= COLOR_TEXTO)
    titulo.pack(pady=10)

    # ---------------- MAIN CONTAINER ----------------
    main_container = ctk.CTkFrame(root, fg_color="transparent")
    main_container.pack(fill="both", expand=True)

    # Configurar grid responsivo
    main_container.grid_rowconfigure(0, weight=1)
    main_container.grid_columnconfigure(0, weight=0)  # Sidebar no se expande
    main_container.grid_columnconfigure(1, weight=1)  # Content sí se expande

    # Colores y botones
    sidebar_buttons = []

    def cambiar_boton_activo(boton_activo):
        for btn in sidebar_buttons:
            if btn == boton_activo:
                btn.configure(fg_color=COLOR_ACTIVO)
            else:
                btn.configure(fg_color=COLOR_INACTIVO)

    
    def create_sidebar_btn(parent, text, image_path, command):
        image = CTkImage(Image.open(image_path), size=(20, 20))
        def wrapped_command():
            cambiar_boton_activo(btn)
            command()
        btn = ctk.CTkButton(parent, text=text, image=image, command=wrapped_command, **btn_style)
        btn.pack(fill="x", padx=10, pady=5)
        return btn

    # ---------------- SIDEBAR ----------------
    sidebar = ctk.CTkFrame(main_container, width=220, fg_color = COLOR_FONDO, corner_radius=0)
    sidebar.grid(row=0, column=0, sticky="ns")

    sidebar_title = ctk.CTkLabel(sidebar, text="MENÚ PRINCIPAL", font=FUENTE_MENU, text_color= COLOR_TEXTO)
    sidebar_title.pack(pady=(20, 10),)
    separator = ctk.CTkFrame(sidebar, height=2, fg_color= COLOR_SEPARADOR)
    separator.pack(fill="x", pady=5, padx=10)
    
    


    # ---------------- CONTENIDO PRINCIPAL ----------------
    content_frame = ctk.CTkFrame(main_container, fg_color= COLOR_INACTIVO)
    content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    # ÁREA DE CONTENIDO DINÁMICO
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    frame_contenido = ctk.CTkFrame(content_frame, corner_radius=15)
    frame_contenido.grid(row=0, column=0, sticky="nsew")

    def abrir_formulario(contenedor):
        for widget in contenedor.winfo_children():
            widget.destroy()
        contenedor.update_idletasks()  # << fuerza refresco visual
        mostrar_formulario_ingresos(contenedor, banco_caja)

    def abrir_inicio(contenedor):
        for widget in contenedor.winfo_children():
            widget.destroy()
        contenedor.update_idletasks()
        mostrar_inicio(contenedor)

    def abrir_formulario_egresos(contenedor):
        for widget in contenedor.winfo_children():
            widget.destroy()
        contenedor.update_idletasks()
        mostrar_formulario_egresos(contenedor)
        
    def abrir_informe_real_ingresos(contenedor):
        for widget in contenedor.winfo_children():
            widget.destroy()
        contenedor.update_idletasks()
        mostrar_informe_real_ingresos(contenedor, clave_cecati)

    def abrir_ajustes(contenedor):
        for widget in contenedor.winfo_children():
            widget.destroy()
        contenedor.update_idletasks()
        mostrar_ajustes(contenedor, clave_cecati, banco_caja)

    def limpiar_contenido():
        for widget in frame_contenido.winfo_children():
            widget.destroy()

    # Botones del sidebar
    btn_inicio_sidebar = create_sidebar_btn(sidebar, "Inicio", "assets/home.png", lambda: abrir_inicio(frame_contenido))
    sidebar_subtitle = ctk.CTkLabel(sidebar, text="Pólizas", font=FUENTE_SUBMENU, text_color= COLOR_TEXTO)
    sidebar_subtitle.pack(pady=5,)
    separator = ctk.CTkFrame(sidebar, height=2, fg_color= COLOR_SEPARADOR)
    separator.pack(fill="x", pady=5, padx=10)
    
    
    btn_ingresos_sidebar = create_sidebar_btn(sidebar, "Ingresos", "assets/increase.png", lambda: abrir_formulario(frame_contenido))
    btn_clientes_sidebar = create_sidebar_btn(sidebar, "Egresos", "assets/decrease.png", lambda: abrir_formulario_egresos(frame_contenido))
    
    sidebar_subtitle = ctk.CTkLabel(sidebar, text="Reportes", font=FUENTE_SUBMENU, text_color= COLOR_TEXTO)
    sidebar_subtitle.pack(pady=5,)
    separator = ctk.CTkFrame(sidebar, height=2, fg_color= COLOR_SEPARADOR)
    separator.pack(fill="x", pady=5, padx=10)
    
    
    btn_reportes_sidebar = create_sidebar_btn(sidebar, "Reportes", "assets/increase.png", lambda: None)
    
    
    sidebar_subtitle = ctk.CTkLabel(sidebar, text="Informes", font= FUENTE_SUBMENU, text_color= COLOR_TEXTO)
    sidebar_subtitle.pack(pady=5,)
    separator = ctk.CTkFrame(sidebar, height=2, fg_color=COLOR_SEPARADOR)
    separator.pack(fill="x", pady=5, padx=10)
    
    btn_inf_real_sidebar = create_sidebar_btn(sidebar, "Informe Real de Ingresos", "assets/report.png", lambda: abrir_informe_real_ingresos(frame_contenido))

    separator = ctk.CTkFrame(sidebar, height=2, fg_color= COLOR_SEPARADOR)
    separator.pack(fill="x", pady=20, padx=10)

    btn_salir_sidebar = create_sidebar_btn(sidebar, "Salir", "assets/exit.png", root.quit)


    btn_config = create_sidebar_btn(sidebar, "Ajustes", "assets/config.png", lambda: abrir_ajustes(frame_contenido))
    
    # Cambio de tema
    modo_claro = [False]
    imagenes = {}

    def cambiar_tema():
        if modo_claro[0]:
            ctk.set_appearance_mode("dark")
            imagenes["tema"] = CTkImage(Image.open("assets/moon.png"), size=(20, 20))
            btn_tema.configure(text="Modo Oscuro", image=imagenes["tema"])
            modo_claro[0] = False
        else:
            ctk.set_appearance_mode("light")
            imagenes["tema"] = CTkImage(Image.open("assets/sun.png"), size=(20, 20))
            btn_tema.configure(text="Modo Claro", image=imagenes["tema"])
            modo_claro[0] = True

    btn_tema = ctk.CTkButton(
        sidebar,
        text="Modo Oscuro",
        command=cambiar_tema,
        image=CTkImage(Image.open("assets/moon.png"), size=(20, 20)),
        **btn_style
    )
    btn_tema.pack(fill="x", padx=10, pady=(5, 20))

    # Cargar pantalla inicial
    abrir_inicio(frame_contenido)
    cambiar_boton_activo(btn_inicio_sidebar)

    root.mainloop()
