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






