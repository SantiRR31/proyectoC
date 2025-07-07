import customtkinter as ctk
from styles.styles import *
from PIL import Image
from customtkinter import CTkImage
import datetime
from functions.funcions import confirmar_aux, confirmar_y_generar2
import requests
from io import BytesIO
import threading
from dotenv import load_dotenv
import os
from utils.rutas import ruta_absoluta
from utils.egresos_utils import confirmar_y_generar_egresos, confirmar_y_generar_consolidado, confirmar_y_generar_infReal
from utils.rutas import ruta_absoluta
from utils.utils import abrir_carpeta
from utils.config_utils import cargar_config

config = cargar_config()

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

    
    clima_frame = ctk.CTkFrame(top_info_frame, fg_color=("#f3f4f6", "#1f2937"), corner_radius=10)
    clima_frame.pack(side="right", padx=10)
    
    clima_content = ctk.CTkFrame(clima_frame, fg_color="transparent")
    clima_content.pack(pady=8, padx=8)
    
    # Crear los labels globales
    clima_icon_label = ctk.CTkLabel(
        clima_content,
        text="",
        width=40,
        height=40
    )
    clima_icon_label.pack(side="right", padx=(0, 8))

    clima_text_label = ctk.CTkLabel(
        clima_content,
        text="Cargando clima...",
        font=("Arial", 12),
        text_color=("#111827", "#f9fafb"),
        justify="left"
    )
    clima_text_label.pack(side="right", fill="x", expand=True)

    # 👉 Esta función SÓLO obtiene datos. No toca la interfaz.
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

    # 👉 Esta función SÍ actualiza la interfaz, con los datos ya obtenidos
    def actualizar_gui_con_clima(datos):
        if datos:
            texto = (
                f"{datos['ciudad']}: {datos['temperatura']}°C, {datos['descripcion']}\n"
                f"Humedad: {datos['humedad']}% | Viento: {datos['viento']} m/s"
            )
            clima_text_label.configure(text=texto)
    
            icono_img = ctk.CTkImage(datos["imagen"], size=(40, 40))
            clima_icon_label.configure(image=icono_img)
            clima_icon_label.image = icono_img  # Referencia para que no se borre
        else:
            clima_text_label.configure(text="Clima no disponible")

    def obtener_clima_seguro():
        try:
            datos = obtener_clima_datos()
        except Exception as e:
            print(f"Error: {e}")
            datos = None

        def actualizar_si_existe():
            if clima_frame.winfo_exists():
                actualizar_gui_con_clima(datos)

        try:
            clima_frame.after(0, actualizar_si_existe)
        except RuntimeError:
            print("No se pudo actualizar la GUI: clima_frame ya no existe.")



    def actualizar_clima(inicial=False):
        # ⚠️ Si ya cerraste la ventana, no lances más hilos
        if not clima_frame.winfo_exists():
            return

        # ✔️ Lanza un hilo solo si el frame todavía existe
        threading.Thread(target=obtener_clima_seguro, daemon=True).start()

        # ⚠️ Programa siguiente actualización solo si la ventana existe
        if inicial:
            clima_frame.after(2000, lambda: actualizar_clima())
        else:
            clima_frame.after(1800000, lambda: actualizar_clima())

    # En el lugar donde inicias el clima:
    actualizar_clima(inicial=True)  # Iniciar el ciclo

    def crear_tarjeta_moderna_con_menu(parent, nombre, icono, color, opciones, boton_texto="Opciones", command=None):
        tarjeta = ctk.CTkFrame(
            parent, 
            fg_color=color[0],
            corner_radius=16,
            border_width=2,
            border_color=color[1],
            width=200, 
            height=220,  # Aumentado para espacio del botón
        )
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
    
    # titulo 
        titulo = ctk.CTkLabel(
            tarjeta,
            text = nombre,
            font=("Arial", 16, "bold"),
            text_color = "#fff",
            wraplength=150,
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
            dropdown_fg_color= "#23232a",
            dropdown_text_color= "#fff",
            font = ("Arial", 12),
            width = 140,
            command=command
        )
        menu.set(boton_texto)
        menu.pack(pady=(0,18))
    
        def on_enter(e):
            tarjeta.configure(fg_color=color[1])
        def on_leave(e):
            tarjeta.configure(fg_color=color[0])
        tarjeta.bind("<Enter>", on_enter)
        tarjeta.bind("<Leave>", on_leave)
    
        return tarjeta
        
    # Sección de tarjetas con diseño más profesional
    tarjetas_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    tarjetas_frame.pack(fill="x", pady=20)

    tarjetas_info = [
        ("Ingresos", "assets/coin.png", ("#10b981", "#059669"), ["Registrar", "Consultar", "Exportar"], "Opciones", None),
        ("Egresos", "assets/wallet.png", ("#ef4444", "#dc2626"), ["LIBRO DE REGISTRO DE EGRESOS"], "Opciones", {"LIBRO DE REGISTRO DE EGRESOS": lambda:confirmar_y_generar_egresos(contenedor_principal=contenedor)}),
        ("Informes", "assets/web.png", ("#8b5cf6", "#7c3aed"), ["Ver", "Descargar"], "Opciones", None),
        ("Inf. Consolidado de Ingresos", "assets/excel.png", ("#0081a8", "#0f6580"), ["Generar"], "Opciones", {"Generar": confirmar_y_generar2}),
        ("Auxiliar Bancario", "assets/coin.png", ("#f59e0b", "#d97706"), ["Generar"], "Opciones", {"Generar": confirmar_aux}),
        ("Inf. Consolidado de egresos", "assets/excel.png", ("#f68b83","#f68b83"), ["Generar"],"Opciones", {"Generar": lambda: confirmar_y_generar_consolidado(contenedor_principal=contenedor)}),
        ("Inf. Real de egresos", "assets/excel.png", ("#55b1bf","#55b1bf"), ["Generar"], "Opciones", {"Generar": lambda: confirmar_y_generar_infReal(contenedor_principal = contenedor)})
    ]
    
    columnas = 4
    
    for col in range(columnas):
            tarjetas_frame.grid_columnconfigure(col, weight=1)
            
    for idx, (nombre, icono, color, opciones, boton_texto, comandos) in enumerate(tarjetas_info):
        fila = idx // columnas
        columna = idx % columnas

        def menu_command(opcion, cmd=comandos, nombre_local=nombre):
            if cmd and opcion in cmd and callable(cmd[opcion]):
                cmd[opcion]()
            else:
                print(f"{nombre_local}: {opcion}")

        tarjeta = crear_tarjeta_moderna_con_menu(
            parent=tarjetas_frame,
            nombre=nombre,
            icono=ruta_absoluta(icono),
            color=color,
            opciones=opciones,
            boton_texto=boton_texto,
            command=menu_command
        )
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")
        
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
    