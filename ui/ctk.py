import customtkinter as ctk
from tkinter import LEFT
from styles.styles import *
from PIL import Image
from customtkinter import CTkImage
import datetime
from functions.funcions import gen_inf_consolidado, confirmar_y_generar, confirmar_aux
import requests
from io import BytesIO
import threading
from dotenv import load_dotenv
import os
from utils.rutas import ruta_absoluta

def mostrar_inicio(contenedor):
    # Configuración del contenedor principal con gradiente sutil
    contenedor.configure(fg_color=("#f8fafc", "#1a1a1a"))
    
    # Frame interno para mejor organización
    main_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Encabezado moderno
    header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 20))

    # Título con efecto moderno
    titulo = ctk.CTkLabel(
        header_frame, 
        text="Sistema de Gestión CECATI 122",
        font=("Arial", 24, "bold"),
        text_color=TEXT_PRIMARY
    )
    titulo.pack(pady=(10, 5))

    # Subtítulo con estilo minimalista
    subtitulo = ctk.CTkLabel(
        header_frame, 
        text="Panel principal del sistema administrativo",
        font=("Arial", 14),
        text_color=("#6b7280", "#9ca3af")
    )
    subtitulo.pack()

    # Sección de widgets superiores
    top_info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    top_info_frame.pack(fill="x", pady=(0, 20))

    # Widget de fecha y hora moderno
    datetime_frame = ctk.CTkFrame(top_info_frame, fg_color=("#ffffff", "#2a2a2a"), corner_radius=12)
    datetime_frame.pack(side="left", padx=10)
    
    # Contenedor para fecha y botón
    fecha_container = ctk.CTkFrame(datetime_frame, fg_color="transparent")
    fecha_container.pack(pady=(10, 0), padx=10, fill="x")

    # Icono de calendario moderno
    calendar_path = ruta_absoluta(os.path.join("assets", "calendar1.png"))
    try:
        if os.path.exists(calendar_path):
            calendar_icon = ctk.CTkImage(
                light_image=Image.open(calendar_path),
                dark_image=Image.open(calendar_path),
                size=(24, 24)
            )
        else:
            raise FileNotFoundError
    except Exception as e:
        print(f"[Error] No se pudo cargar el icono: {str(e)}")
        calendar_icon = None
        calendar_text = "📅"
    else:
        calendar_text = ""

    calendario_btn = ctk.CTkButton(
        fecha_container,
        text=calendar_text,
        image=calendar_icon,
        width=30,
        height=30,
        corner_radius=8,
        fg_color="transparent",
        hover_color=("#e5e7eb", "#3d3d3d"),
        command=lambda: mostrar_calendario(fecha_label)
    )
    calendario_btn.pack(side="right")

    fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
    fecha_label = ctk.CTkLabel(
        fecha_container,
        text=fecha_actual,
        font=("Arial", 14, "bold"),
        text_color=("#111827", "#f9fafb")
    )
    fecha_label.pack(side="left", padx=(0, 10))

    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
    hora_label = ctk.CTkLabel(
        datetime_frame,
        text=hora_actual,
        font=("Arial", 16, "bold"),
        text_color=("#3b82f6", "#60a5fa")
    )
    hora_label.pack(pady=(0, 10), padx=10)

    def actualizar_hora():
        ahora = datetime.datetime.now()
        hora_label.configure(text=ahora.strftime("%H:%M:%S"))
        hora_label.after(1000, actualizar_hora)
    
    actualizar_hora()

    # Widget de clima modernizado
    clima_frame = ctk.CTkFrame(top_info_frame, fg_color=("#ffffff", "#2a2a2a"), corner_radius=12)
    clima_frame.pack(side="left", padx=10)
    
    clima_content = ctk.CTkFrame(clima_frame, fg_color="transparent")
    clima_content.pack(pady=10, padx=10)

    clima_icon_label = ctk.CTkLabel(clima_content, text="", width=40, height=40)
    clima_icon_label.pack(side="left", padx=(0, 10))

    clima_text_frame = ctk.CTkFrame(clima_content, fg_color="transparent")
    clima_text_frame.pack(side="left")

    ciudad_label = ctk.CTkLabel(
        clima_text_frame,
        text="Tequisquiapan",
        font=("Arial", 12, "bold"),
        text_color=("#111827", "#f9fafb")
    )
    ciudad_label.pack(anchor="w")

    temp_label = ctk.CTkLabel(
        clima_text_frame,
        text="Cargando...",
        font=("Arial", 14),
        text_color=("#3b82f6", "#60a5fa")
    )
    temp_label.pack(anchor="w")

    detalles_label = ctk.CTkLabel(
        clima_text_frame,
        text="",
        font=("Arial", 11),
        text_color=("#6b7280", "#9ca3af")
    )
    detalles_label.pack(anchor="w")

    # Widget de estado del sistema moderno
    estado_frame = ctk.CTkFrame(top_info_frame, fg_color=("#ffffff", "#2a2a2a"), corner_radius=12)
    estado_frame.pack(side="right", padx=10)

    estado_icon = ctk.CTkLabel(
        estado_frame,
        text="✓",
        font=("Arial", 24),
        text_color=("#10b981", "#059669")
    )
    estado_icon.pack(pady=(10, 5))

    estado_label = ctk.CTkLabel(
        estado_frame,
        text="Sistema Operativo",
        font=("Arial", 12, "bold"),
        text_color=("#6b7280", "#9ca3af")
    )
    estado_label.pack(pady=(0, 10))

    # Sección de tarjetas modernizadas
    tarjetas_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    tarjetas_frame.pack(fill="both", expand=True, pady=20)

    # Nueva función para tarjetas modernas
    def crear_tarjeta_moderna(parent, titulo, icono, color_bg, color_hover, opciones=None, comando=None):
        tarjeta = ctk.CTkFrame(
            parent,
            width=200,
            height=220,
            corner_radius=16,
            border_width=0,
            fg_color=color_bg
        )
        
        # Contenedor del icono con efecto de elevación
        icono_frame = ctk.CTkFrame(
            tarjeta,
            width=60,
            height=60,
            corner_radius=12,
            fg_color=( "#ffffff","#18181b")
        )
        icono_frame.pack(pady=(20, 15))
        
        try:
            icon_img = ctk.CTkImage(Image.open(icono), size=(32, 32))
            ctk.CTkLabel(icono_frame, image=icon_img, text="").place(relx=0.5, rely=0.5, anchor="center")
        except:
            ctk.CTkLabel(icono_frame, text="📊", font=("Arial", 24)).place(relx=0.5, rely=0.5, anchor="center")
        
        # Título de la tarjeta
        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=("Arial", 14, "bold"),
            text_color=("#ffffff", "#ffffff"),
            wraplength=160,
            justify="center"
        ).pack(pady=(0, 15))
        
        # Botón de acción con efecto hover
        boton = ctk.CTkButton(
            tarjeta,
            text="Acceder",
            font=("Arial", 12),
            fg_color="transparent",
            hover_color=color_hover,
            border_width=2,
            border_color=color_hover,
            corner_radius=8,
            command=lambda: mostrar_menu_opciones(titulo, opciones, comando) if opciones else comando() if comando else None
        )
        boton.pack(pady=(0, 20), padx=20, fill="x")
        
        # Efectos hover
        def on_enter(e):
            tarjeta.configure(fg_color=color_hover)
            icono_frame.configure(fg_color=("#ffffff","#18181b"))
        
        def on_leave(e):
            tarjeta.configure(fg_color=color_bg)
            icono_frame.configure(fg_color=("#ffffff","#18181b"))
        
        tarjeta.bind("<Enter>", on_enter)
        tarjeta.bind("<Leave>", on_leave)
        
        return tarjeta

    def mostrar_menu_opciones(titulo, opciones, comando):
        menu = ctk.CTkToplevel()
        menu.title(f"Opciones - {titulo}")
        menu.geometry("300x200")
        menu.grab_set()
        
        ctk.CTkLabel(
            menu,
            text=f"Seleccione una opción para\n{titulo}",
            font=("Arial", 14),
            justify="center"
        ).pack(pady=20)
        
        for opcion in opciones:
            ctk.CTkButton(
                menu,
                text=opcion,
                command=lambda o=opcion: (comando(o) if comando else None, menu.destroy()),
                corner_radius=8
            ).pack(pady=5, padx=50, fill="x")

    # Configuración de la cuadrícula para las tarjetas
    columnas = 3
    for col in range(columnas):
        tarjetas_frame.grid_columnconfigure(col, weight=1)
    
    filas = 2
    for row in range(filas):
        tarjetas_frame.grid_rowconfigure(row, weight=1)

    # Datos para las tarjetas modernas
    tarjetas_info = [
        {
            "titulo": "Ingresos",
            "icono": ruta_absoluta("assets/coin.png"),
            "color_bg": ("#3b82f6", "#1d4ed8"),
            "color_hover": ("#60a5fa", "#1e40af"),
            "opciones": ["Registrar", "Consultar", "Exportar"],
            "comando": lambda opcion, titulo="Ingresos": print(f"{titulo}: {opcion}")
        },
        {
            "titulo": "Egresos",
            "icono": ruta_absoluta("assets/wallet.png"),
            "color_bg": ("#ef4444", "#b91c1c"),
            "color_hover": ("#f87171", "#991b1b"),
            "opciones": ["Registrar", "Consultar", "Exportar"],
            "comando": lambda opcion, titulo="Egresos": print(f"{titulo}: {opcion}")
        },
        {
            "titulo": "Reportes",
            "icono": ruta_absoluta("assets/iconuse.png"),
            "color_bg": ("#10b981", "#047857"),
            "color_hover": ("#34d399", "#065f46"),
            "opciones": ["Ver", "Descargar"],
            "comando": lambda opcion, titulo="Reportes": print(f"{titulo}: {opcion}")
        },
        {
            "titulo": "Informes",
            "icono": ruta_absoluta("assets/web.png"),
            "color_bg": ("#8b5cf6", "#6d28d9"),
            "color_hover": ("#a78bfa", "#5b21b6"),
            "opciones": ["Ver", "Descargar"],
            "comando": lambda opcion, titulo="Informes": print(f"{titulo}: {opcion}")
        },
        {
            "titulo": "Inf. Consolidado",
            "icono": ruta_absoluta("assets/excel.png"),
            "color_bg": ("#f59e0b", "#b45309"),
            "color_hover": ("#fbbf24", "#92400e"),
            "opciones": ["Generar"],
            "comando": lambda opcion: confirmar_y_generar() if opcion == "Generar" else None
        },
        {
            "titulo": "Auxiliar Bancario",
            "icono": ruta_absoluta("assets/coin.png"),
            "color_bg": ("#ec4899", "#be185d"),
            "color_hover": ("#f472b6", "#9d174d"),
            "opciones": ["Generar"],
            "comando": lambda opcion: confirmar_aux() if opcion == "Generar" else None
        }
    ]

    # Crear y colocar las tarjetas
    for idx, tarjeta_data in enumerate(tarjetas_info):
        fila = idx // columnas
        columna = idx % columnas
        
        tarjeta = crear_tarjeta_moderna(
            parent=tarjetas_frame,
            titulo=tarjeta_data["titulo"],
            icono=tarjeta_data["icono"],
            color_bg=tarjeta_data["color_bg"],
            color_hover=tarjeta_data["color_hover"],
            opciones=tarjeta_data["opciones"],
            comando=tarjeta_data["comando"]
        )
        tarjeta.grid(
            row=fila, 
            column=columna, 
            padx=15, 
            pady=15, 
            sticky="nsew"
        )

    # Función para mostrar calendario (mejorada)
    def mostrar_calendario(label_fecha):
        popup = ctk.CTkToplevel()
        popup.title("Calendario")
        popup.geometry("300x300")
        popup.resizable(False, False)
        popup.grab_set()
        
        try:
            from tkcalendar import Calendar
            cal = Calendar(
                popup, 
                selectmode="day",
                date_pattern="dd/mm/yyyy",
                background="#ffffff" if ctk.get_appearance_mode() == "Light" else "#2a2a2a",
                foreground="black" if ctk.get_appearance_mode() == "Light" else "white",
                bordercolor="#e5e7eb",
                headersbackground="#f3f4f6",
                normalbackground="#ffffff",
                weekendbackground="#f3f4f6",
                selectbackground="#3b82f6"
            )
            cal.pack(pady=20, padx=20, fill="both", expand=True)
            
            def on_date_select():
                label_fecha.configure(text=cal.get_date())
                popup.destroy()
                
            ctk.CTkButton(
                popup,
                text="Seleccionar",
                command=on_date_select,
                corner_radius=8
            ).pack(pady=(0, 20))
            
        except ImportError:
            ctk.CTkLabel(
                popup,
                text="Instale tkcalendar:\npip install tkcalendar",
                justify="center"
            ).pack(expand=True)
            
            popup.after(3000, popup.destroy)

    # Función para actualizar el clima (mejorada)
    def actualizar_gui_con_clima(datos):
        if datos:
            ciudad_label.configure(text=datos['ciudad'])
            temp_label.configure(text=f"{datos['temperatura']}°C | {datos['descripcion'].capitalize()}")
            detalles_label.configure(text=f"Humedad: {datos['humedad']}% | Viento: {datos['viento']} m/s")
            
            icono_img = ctk.CTkImage(datos["imagen"], size=(40, 40))
            clima_icon_label.configure(image=icono_img)
            clima_icon_label.image = icono_img
        else:
            ciudad_label.configure(text="Tequisquiapan")
            temp_label.configure(text="Datos no disponibles")
            detalles_label.configure(text="")
            
    def obtener_clima_datos():
        ciudad = 'Tequisquiapan'
        load_dotenv()  # Cargar variables de entorno desde .env
        API_KEY = os.getenv("API_KEY")
        url = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es'
        try:
            respuesta = requests.get(url, timeout=10)
            datos = respuesta.json()

            if datos.get("main"):
                temperatura = datos["main"]["temp"]
                descripcion = datos["weather"][0]["description"]
                humedad = datos["main"]["humidity"]
                viento = datos["wind"]["speed"]
                icono = datos["weather"][0]["icon"]

                # Cargar la imagen del icono
                icon_url = f"http://openweathermap.org/img/wn/{icono}@2x.png"
                icon_response = requests.get(icon_url)
                imagen = Image.open(BytesIO(icon_response.content))
                imagen = imagen.resize((40, 40), Image.Resampling.LANCZOS)

                return {
                    "ciudad": ciudad,
                    "temperatura": temperatura,
                    "descripcion": descripcion,
                    "humedad": humedad,
                    "viento": viento,
                    "imagen": imagen
                }
        except:
            return None


    # Iniciar la actualización del clima
    threading.Thread(target=obtener_clima_datos, daemon=True).start()