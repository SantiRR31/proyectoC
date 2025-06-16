#--- Fuentes --------
FUENTE_TEXTO = ("Arial", 14, "bold")
FUENTE_SUBTITULO = ("Arial", 12)


COLOR_TEXTO_SEMIVISIBLE = ("#94a3b8", "#cbd5e1")
COLOR_TEXTO = ("#121212", "#f1f5f9")
COLOR_TEXTO_APARTADO = ("#334155", "#475569")
COLOR_TEXTO_APARTADO_SECUNDARIO = ("#64748b", "#94a3b8")

#--- Colores --------

COLOR_PRIMARIO = ("#cc3d42", "#cc3d42")
COLOR_CONT_PRIMARIO = ("#faf7f6", "#191919")
COLOR_CONT_SECUNDARIO = ("#ddd9d9", "#1c1c1c")

COLOR_FONDO = ("#cc3d42", "#cc3d42")
BG_COLOR = ("#f9f9f9", "#121212")
SURFACE_COLOR = ("#ffffff", "#1e1e1e")

TEXT_PRIMARY = ("#d21329")
TEXT_SECONDARY = ("#4d4d4d", "#cccccc")
TEXT_DISABLED = ("#a3a3a3", "#6b6b6b")

SEPARATOR = ("#dcdcdc", "#2a2a2a")
SEPARATOR_LIGHT = ("#f0f0f0", "#3a3a3a")

PRIMARY_COLOR = ("#cc3d42", "#cc3d42")
ACCENT_COLOR = ("#e57373", "#ff999c")
BORDER_COLOR = ("#dcdcdc", "#2a2a2a")

COLOR_VALIDACION_OK = ("#008d62", "#00b27a")
COLOR_VALIDACION_ERROR = ("#d10d2f", "#ff4056")
COLOR_VALIDACION_NEUTRO = ("gray", "#a0a0a0")

# Colores globales adicionales
COLOR_ACTIVO = "#5b44e0"
COLOR_INACTIVO = "transparent"
FONDO_CONTENEDORES = "transparent"
COLOR_SEPARADOR = SEPARATOR
COLOR_TEXTO = ("#121212", "#e6e9f0")
ENTRADA_FRAME_C = FONDO_CONTENEDORES  # igual que fondo de contenedores

NAVBAR_COLOR = "#e6e9f0"

# --- FUENTES ---
FUENTE_TITULO = ("Arial", 24, "bold")
FUENTE_FORMULARIO_T = ("Arial", 28, "bold")
FUENTE_MENU = ("Arial", 16, "bold")
FUENTE_TOTAL = ("Arial", 16)
FUENTE_VALIDACION = ("Arial", 20)
FUENTE_SECCION_TITULO = ("Arial", 14, "bold")
FUENTE_LABEL = ("Arial", 14)
FUENTE_SUBMENU = ("Arial", 12)
FUENTE_FORMULARIO_S = ("Arial", 16)
FUENTE_BOTON = ("Arial", 14)

# --- TAMAÑOS Y RADIOS ---
RADIO_BOTON = 5
RADIO_CONTENEDORES = 15
RADIO_BOTON_AGREGAR = 32




#-- ESTILOS DE ENTRADAS ---
ESTILO_ENTRADA = {
    "font": ("Arial", 14),
    "text_color": COLOR_TEXTO,
    "fg_color": FONDO_CONTENEDORES,
    "border_color": BORDER_COLOR,
    "corner_radius": RADIO_CONTENEDORES,
    "height": 40,
    "width": 200
}

# --- ESTILOS DE BOTONES ---
btn_sidebar_style = {
    "font": ("Arial", 14),
    "text_color": "white",
    "fg_color": "transparent",
    "hover_color": "#3c5ea5",
    "corner_radius": 10,
    "height": 40,
    "anchor": "w"
}

btn_inactivo_style = {
    "fg_color": COLOR_INACTIVO,
    "hover_color": "#34495e",
    "text_color": "white",
    "anchor": "w",
    "font": ("Arial", 14),
    "height": 40,
    "corner_radius": 5
}

btn_primario = {
    "corner_radius": 10,
    "fg_color": "#007acc",
    "hover_color": "#005f99",
    "text_color": "white",
    "font": ("Arial", 14),
    "height": 35,
    "width": 160
}

btn_secundario = {
    "corner_radius": 10,
    "fg_color": "#d9d9d9",
    "hover_color": "#c0c0c0",
    "text_color": "black",
    "font": ("Arial", 14),
    "height": 35,
    "width": 160
}

btn_eliminar_style = {
    "width": 30,
    "fg_color": "#d10d2f",
    "hover_color": "#d93954",
    "corner_radius": 5
}

btn_agregar_style = {
    "corner_radius": RADIO_BOTON_AGREGAR,
    "fg_color": "#008d62",
    "hover_color": "#2ca880"
}

btn_guardar_style = {
    "width": 120,
    "fg_color": "#004b8f",
    "hover_color": "#0065a5",
    "corner_radius": RADIO_BOTON_AGREGAR
}

btn_descargar_style = {
    "width": 120,
    "fg_color": "#008d62",
    "hover_color": "#2ca880",
    "corner_radius": RADIO_BOTON_AGREGAR
}

# Configuración de estilos consistentes
ESTILO_FRAME = {
    "corner_radius": 12,
    "fg_color": ("#f9fafb", "#1c1c1c"),
    ##"border_width": 1,
    ##"border_color": ("#e5e7eb", "#374151")
}
    
ESTILO_ENTRADA = {
    "height": 35,
    "font": FUENTE_TEXTO,
    "border_width": 1,
    "border_color": ("#d1d5db", "#545454"),
    "fg_color": ("#ffffff", "#212121"),
    "text_color": ("#111827", "#f3f4f6")
}
    
ESTILO_BOTON = {
    #"font": FUENTE_BOTON,
    "height": 35,
    "corner_radius": 8
}

ESTILO_LIST_SUG = {
    "height":6,
    "bg":"#ffffff",
    "fg":"#111827",
    "selectbackground":"#3b82f6",
    "selectforeground":"#ffffff",
    "font":("Arial", 10),
    "highlightthickness":1,
    "highlightcolor":"#3b82f6",
    "activestyle":"dotbox",
    "relief":"solid",
    "borderwidth":1
}