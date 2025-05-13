import tkinter as tk
import customtkinter as ctk
from ui.formIngresosDiarios import mostrar_formulario_ingresos
from styles.styles import estilo_btn

def lanzar_ventana_principal():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    
    root = ctk.CTk()

# Obtener tamaño de pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

# Establecer tamaño de ventana
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.title("Ventana Principal")


    # ---------------- HEADER ----------------
    header = ctk.CTkFrame(root, height=60, fg_color="#1E90FF")
    header.pack(fill="x")
    titulo = ctk.CTkLabel(header, text="Sistema de Gestión", font=("Arial", 24, "bold"), text_color="white")
    titulo.pack(pady=10)

    # ---------------- NAVBAR ----------------
    navbar = ctk.CTkFrame(root, fg_color="#e6e9f0", height=60, corner_radius=0)
    navbar.pack(fill="x", padx=0, pady=0)

    def abrir_formulario():
        mostrar_formulario_ingresos(frame_contenido)

    def mostrar_inicio():
        limpiar_contenido()
        etiqueta = ctk.CTkLabel(frame_contenido, text="Bienvenido", font=("Arial", 22))
        etiqueta.pack(pady=60)

    def limpiar_contenido():
        for widget in frame_contenido.winfo_children():
            widget.destroy()

# Sub-frame para centrar los botones dentro del navbar
    navbar_inner = ctk.CTkFrame(navbar, fg_color="transparent")
    navbar_inner.pack(pady=10)

    

    btn_inicio = ctk.CTkButton(navbar_inner, text="🏠 Inicio", command=mostrar_inicio, **estilo_btn )
    btn_inicio.pack(side="left", padx=10)

    btn_formulario = ctk.CTkButton(navbar_inner, text="📄 Ingresos Diarios", command=abrir_formulario, **estilo_btn)
    btn_formulario.pack(side="left", padx=10)

    btn_reservado1 = ctk.CTkButton(navbar_inner, text="🔧 Otra Sección", command=lambda: None, **estilo_btn)
    btn_reservado1.pack(side="left", padx=10)

    btn_reservado2 = ctk.CTkButton(navbar_inner, text="➕ Nuevo Módulo", command=lambda: None, **estilo_btn)
    btn_reservado2.pack(side="left", padx=10)


    # ---------------- CONTENIDO ----------------
    frame_contenido = ctk.CTkFrame(root, corner_radius=15)
    frame_contenido.pack(expand=True, fill="both", padx=20, pady=20)

    # Mostrar contenido inicial
    mostrar_inicio()

    # ---------------- MENÚ ----------------
    menu = tk.Menu(root)
    root.config(menu=menu)
    menu_archivo = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Archivo", menu=menu_archivo)
    menu_archivo.add_command(label="Abrir Formulario", command=abrir_formulario)
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Salir", command=root.quit)

    root.mainloop()
