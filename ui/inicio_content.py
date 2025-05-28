import customtkinter as ctk
from tkinter import LEFT
from styles.styles import *
from PIL import Image
from customtkinter import CTkImage

def mostrar_inicio(contenedor):
    # Configuración del contenedor principal con gradiente sutil
    
    # Frame interno para mejor organización
    main_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
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

    # Sección de tarjetas con diseño más profesional
    tarjetas_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    tarjetas_frame.pack(fill="x", pady=20)

    # Tarjetas con efecto hover y sombra
    for i, (nombre, icono, color) in enumerate([
        ("Ingresos", "assets/coin.png", ("#10b981", "#059669")),
        ("Egresos", "assets/wallet.png", ("#ef4444", "#dc2626")),
        ("Reportes", "assets/iconuse.png", ("#3b82f6", "#2563eb")),
        ("Informes", "assets/web.png", ("#8b5cf6", "#7c3aed"))
    ]):
        tarjeta = crear_tarjeta_moderna(tarjetas_frame, nombre, icono, color)
        tarjeta.grid(row=0, column=i, padx=15, pady=10, sticky="nsew")
        tarjetas_frame.grid_columnconfigure(i, weight=1)

    # Área informativa
    info_frame = ctk.CTkFrame(
        main_frame, 
        fg_color=("#ffffff", "#1e293b"), 
        corner_radius=12
    )
    info_frame.pack(fill="x", pady=(20, 10), padx=5)

    info_label = ctk.CTkLabel(
        info_frame,
        text=(
            "Bienvenido al sistema de control administrativo del CECATI 122\n\n"
            "Este sistema está diseñado para optimizar tus procesos diarios, mantener\n"
            "el control financiero institucional y generar reportes automatizados.\n\n"
            "Selecciona una opción del menú lateral para comenzar."
        ),
        font=("Arial", 14),
        text_color=("#374151", "#f3f4f6"),
        justify="center",
        wraplength=600
    )
    info_label.pack(pady=30, padx=20)

    # Imagen decorativa con borde redondeado
    try:
        imagen = CTkImage(Image.open("assets/cecati122.png"), size=(500, 500))
        img_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        img_frame.pack(pady=(10, 0))

        img_label = ctk.CTkLabel(
            img_frame, 
            image=imagen, 
            text=""
        )
        img_label.pack()
    except Exception as e:
        print("No se pudo cargar la imagen:", e)

def crear_tarjeta_moderna(master, texto, icono_path, color):
    frame = ctk.CTkFrame(
        master, 
        width=180, 
        height=180, 
        fg_color=("#ffffff", "#1c1c1c"),
        border_color=color,
        border_width=2,
        corner_radius=18
    )
    
    # Contenido de la tarjeta
    content_frame = ctk.CTkFrame(frame, fg_color="transparent")
    content_frame.pack(expand=True, fill="both", padx=10, pady=10)
    
    try:
        icono = CTkImage(Image.open(icono_path), size=(60, 60))
        icono_label = ctk.CTkLabel(
            content_frame, 
            image=icono, 
            text=""
        )
        icono_label.pack(pady=(15, 10))
    except Exception as e:
        print(f"No se pudo cargar el ícono {icono_path}: {e}")
        # Icono alternativo
        icono_label = ctk.CTkLabel(
            content_frame, 
            text="📊",
            font=("Arial", 30),
            text_color=color[0]
        )
        icono_label.pack(pady=(15, 10))

    texto_label = ctk.CTkLabel(
        content_frame, 
        text=texto, 
        font=("Arial", 16, "bold"), 
        text_color=("#111827", "#f9fafb")
    )
    texto_label.pack(pady=(0, 15))
    
    # Efecto hover
    def on_enter(e):
        frame.configure(fg_color=("#f9fafb", "#334155"))
    
    def on_leave(e):
        frame.configure(fg_color=("#ffffff", "#1c1c1c"))
    
    frame.bind("<Enter>", on_enter)
    frame.bind("<Leave>", on_leave)
    
    return frame
