import customtkinter as ctk
from tkinter import LEFT
from styles.styles import *
from PIL import Image
from customtkinter import CTkImage
import datetime

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

    # Sección superior con información útil
    top_info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    top_info_frame.pack(fill="x", pady=(0, 20))

    # Widget de fecha y hora actual
    datetime_frame = ctk.CTkFrame(top_info_frame, fg_color=("#f3f4f6", "#1f2937"), corner_radius=10)
    datetime_frame.pack(side="left", padx=10)

    fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

    fecha_label = ctk.CTkLabel(
        datetime_frame,
        text=fecha_actual,
        font=("Arial", 14, "bold"),
        text_color=("#111827", "#f9fafb")
    )
    fecha_label.pack(pady=(10, 0), padx=15)

    hora_label = ctk.CTkLabel(
        datetime_frame,
        text=hora_actual,
        font=("Arial", 16),
        text_color=("#4b5563", "#d1d5db")
    )
    hora_label.pack(pady=(0, 10), padx=15)

    # Actualizar la hora cada segundo
    def actualizar_hora():
        ahora = datetime.datetime.now()
        hora_label.configure(text=ahora.strftime("%H:%M:%S"))
        hora_label.after(1000, actualizar_hora)
    
    actualizar_hora()

    # Widget de estado del sistema
    estado_frame = ctk.CTkFrame(top_info_frame, fg_color=("#f3f4f6", "#1f2937"), corner_radius=10)
    estado_frame.pack(side="right", padx=10)

    estado_label = ctk.CTkLabel(
        estado_frame,
        text="Estado del sistema:",
        font=("Arial", 12),
        text_color=("#6b7280", "#9ca3af")
    )
    estado_label.pack(pady=(5, 0), padx=15)

    estado_valor = ctk.CTkLabel(
        estado_frame,
        text="✔ Operativo",
        font=("Arial", 14, "bold"),
        text_color=("#10b981", "#059669")
    )
    estado_valor.pack(pady=(0, 5), padx=15)

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

    # Área informativa con pestañas
    tabview = ctk.CTkTabview(
        main_frame,
        fg_color=("#ffffff", "#1e293b"),
        segmented_button_fg_color=("#e5e7eb", "#374151"),
        segmented_button_selected_color=("#3b82f6", "#2563eb"),
        segmented_button_selected_hover_color=("#2563eb", "#1d4ed8"),
        width=600,
        height=180
    )
    tabview.pack(pady=(20, 10), padx=5)
    
    # Añadir pestañas
    tabview.add("Bienvenida")
    tabview.add("Noticias")
    tabview.add("Recordatorios")

    # Contenido de la pestaña de bienvenida
    bienvenida_content = ctk.CTkLabel(
        tabview.tab("Bienvenida"),
        text=(
            "Bienvenido al sistema de control administrativo del CECATI 122\n\n"
            "Este sistema está diseñado para optimizar tus procesos diarios, mantener\n"
            "el control financiero institucional y generar reportes automatizados.\n\n"
            "Selecciona una opción del menú lateral para comenzar."
        ),
        font=("Arial", 14),
        text_color=("#374151", "#f3f4f6"),
        justify="center",
        wraplength=550
    )
    bienvenida_content.pack(pady=20, padx=10)

    # Contenido de la pestaña de noticias
    noticias_content = ctk.CTkLabel(
        tabview.tab("Noticias"),
        text=(
            "Últimas actualizaciones del sistema:\n\n"
            "• Versión 2.1 del sistema instalada\n"
            "• Nuevo módulo de reportes disponible\n"
            "• Mantenimiento programado para el próximo viernes"
        ),
        font=("Arial", 14),
        text_color=("#374151", "#f3f4f6"),
        justify="left",
        wraplength=550
    )
    noticias_content.pack(pady=20, padx=10)

    # Contenido de la pestaña de recordatorios
    recordatorios_content = ctk.CTkLabel(
        tabview.tab("Recordatorios"),
        text=(
            "Recordatorios importantes:\n\n"
            "• Reporte mensual pendiente de enviar\n"
            "• Revisar ingresos de la semana\n"
            "• Verificar egresos no categorizados"
        ),
        font=("Arial", 14),
        text_color=("#374151", "#f3f4f6"),
        justify="left",
        wraplength=550
    )
    recordatorios_content.pack(pady=20, padx=10)

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