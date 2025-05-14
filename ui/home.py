import tkinter as tk
import customtkinter as ctk
from ui.formIngresosDiarios import mostrar_formulario_ingresos
from styles.styles import estilo_btn
from ui.inicio_content import mostrar_inicio

def lanzar_ventana_principal():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    # Obtener tamaño de pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.title("Ventana Principal")

    # ---------------- HEADER ----------------
    header = ctk.CTkFrame(root, height=60, fg_color="#1E90FF", corner_radius=0)
    header.pack(fill="x")
    titulo = ctk.CTkLabel(header, text="Sistema de Gestión", font=("Arial", 24, "bold"), text_color="white")
    titulo.pack(pady=10)

    # ---------------- MAIN CONTAINER ----------------
    main_container = ctk.CTkFrame(root, fg_color="transparent")
    main_container.pack(fill="both", expand=True)

    # ---------------- SIDEBAR ----------------
    sidebar = ctk.CTkFrame(main_container, width=220, fg_color="#2c3e50", corner_radius=0)
    sidebar.pack(side="left", fill="y", padx=0, pady=0)

    sidebar_title = ctk.CTkLabel(sidebar, text="MENÚ PRINCIPAL", font=("Arial", 16, "bold"), text_color="white")
    sidebar_title.pack(pady=(20, 30), padx=10)

    btn_style = {
        "fg_color": "transparent",
        "hover_color": "#34495e",
        "text_color": "white",
        "anchor": "w",
        "font": ("Arial", 14),
        "height": 40,
        "corner_radius": 5
    }

    def create_sidebar_btn(parent, text, icon, command):
        btn = ctk.CTkButton(parent, text=f"  {icon}  {text}", command=command, **btn_style)
        btn.pack(fill="x", padx=10, pady=5)
        return btn

    # ---------------- CONTENIDO PRINCIPAL ----------------
    content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
    content_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

    # ---------------- ÁREA DE CONTENIDO DINÁMICO ----------------
    frame_contenido = ctk.CTkFrame(content_frame, corner_radius=15)
    frame_contenido.pack(expand=True, fill="both")

    # ---------------- FUNCIONES ----------------
    def abrir_formulario(contenedor):
        for widget in contenedor.winfo_children():
            widget.destroy()
        mostrar_formulario_ingresos(contenedor)

    def abrir_inicio(contenedor):
        for widget in contenedor.winfo_children():
            widget.destroy()
        mostrar_inicio(contenedor)

    def limpiar_contenido():
        for widget in frame_contenido.winfo_children():
            widget.destroy()

    # ---------------- BOTONES DEL SIDEBAR ----------------
    btn_inicio_sidebar = create_sidebar_btn(sidebar, "Inicio", "🏠", lambda: abrir_inicio(frame_contenido))
    btn_ingresos_sidebar = create_sidebar_btn(sidebar, "Ingresos Diarios", "📊", lambda: abrir_formulario(frame_contenido))
    btn_clientes_sidebar = create_sidebar_btn(sidebar, "Clientes", "👥", lambda: None)
    btn_reportes_sidebar = create_sidebar_btn(sidebar, "Reportes", "📈", lambda: None)
    btn_config_sidebar = create_sidebar_btn(sidebar, "Configuración", "⚙️", lambda: None)

    separator = ctk.CTkFrame(sidebar, height=2, fg_color="#34495e")
    separator.pack(fill="x", pady=20, padx=10)

    btn_salir_sidebar = create_sidebar_btn(sidebar, "Cerrar Sesión", "🚪", root.quit)

    # Mostrar contenido inicial
    abrir_inicio(frame_contenido)

    root.mainloop()
