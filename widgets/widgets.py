from datetime import datetime
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

# Funciones para crear widgets modulares
def crear_label(parent, text, font, **grid_opts):
    label = ctk.CTkLabel(parent, text=text, font=font)
    label.grid(**grid_opts)
    return label

def crear_entry(parent, placeholder, row, column, **grid_opts):
    entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
    entry.grid(row=row, column=column, **grid_opts)
    return entry

def crear_boton(parent, text, command, style, **pack_opts):
    btn = ctk.CTkButton(parent, text=text, command=command, **style)
    btn.pack(**pack_opts)
    return btn

def crear_boton_imagen(parent, text, image_path, style, command, **pack_opts):
    img = Image.open(image_path)
    btn = ctk.CTkButton(parent, text=text, image=CTkImage(img, size=(20, 20)), command=command, **style)
    btn.pack(**pack_opts)
    return btn

def ventana_seleccion_mes_anio_y_campos(
    titulo: str,
    funcion_generar,
    contenedor_principal=None,
    anios_rango: tuple[int, int] = None,
    meses_lista: list[str] = None,
    campos_adicionales: list[dict] = None,
    validar_campos_adicionales=None,
    ancho_ventana: str = "340x230",
):
    import tkinter.messagebox as messagebox

    if anios_rango is None:
        anio_actual = datetime.now().year
        anios_rango = (anio_actual - 5, anio_actual + 1)
    else:
        anio_actual = anios_rango[1]

    if meses_lista is None:
        meses_lista = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]

    ventana = ctk.CTkToplevel()
    ventana.title(titulo)
    ventana.geometry(ancho_ventana)
    ventana.resizable(False, False)
    ventana.grab_set()
    if contenedor_principal:
        ventana.transient(contenedor_principal)

    ctk.CTkLabel(ventana, text="Seleccione el mes y año del reporte:", font=("Arial", 13)).pack(pady=(16, 6))

    frame = ctk.CTkFrame(ventana, fg_color="transparent")
    frame.pack(pady=4)

    mes_var = ctk.StringVar(value=meses_lista[datetime.now().month - 1])
    anio_var = ctk.StringVar(value=str(anio_actual))

    mes_cb = ttk.Combobox(frame, values=meses_lista, textvariable=mes_var, state="readonly", width=14)
    mes_cb.grid(row=0, column=0, padx=8)

    anios_valores = [str(a) for a in range(anios_rango[0], anios_rango[1] + 1)]
    anio_cb = ttk.Combobox(frame, values=anios_valores, textvariable=anio_var, width=8, state="readonly")
    anio_cb.grid(row=0, column=1, padx=8)

    # Diccionario para variables adicionales (stringvar, intvar, etc)
    vars_adicionales = {}

    if campos_adicionales:
        frame_adicional = ctk.CTkFrame(ventana, fg_color="transparent")
        frame_adicional.pack(pady=8)

        for idx, campo in enumerate(campos_adicionales):
            label_text = campo.get("label", f"Campo {idx}")
            var = campo.get("variable")
            if var is None:
                var = ctk.StringVar()
            vars_adicionales[label_text] = var

            ctk.CTkLabel(frame_adicional, text=label_text + ":", font=("Arial", 12)).grid(row=idx, column=0, padx=8, pady=4)
            entry_widget = campo.get("widget", ctk.CTkEntry)
            w = entry_widget(frame_adicional, textvariable=var, width=120)
            w.grid(row=idx, column=1, padx=8, pady=4)

    def ejecutar_generacion():
        mes_idx = meses_lista.index(mes_var.get()) + 1
        anio = int(anio_var.get())
        mes_anio = f"{anio}-{mes_idx:02d}"

        # Validar campos adicionales si hay función definida
        if validar_campos_adicionales:
            valido, mensaje = validar_campos_adicionales(vars_adicionales)
            if not valido:
                messagebox.showerror("Error", mensaje)
                return

        ventana.destroy()

        # Ejecutar la función generadora pasando mes_anio y variables extras
        funcion_generar(mes_anio, vars_adicionales)

    ctk.CTkButton(ventana, text="Generar", command=ejecutar_generacion).pack(pady=18)
