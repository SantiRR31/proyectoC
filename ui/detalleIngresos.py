import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from widgets.widgets import *
from styles.styles import *
from utils.config_utils import cargar_config
import sqlite3
from tkinter import messagebox


def mostrar_detalles_ingresos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()

    config = cargar_config()

    ctk.CTkLabel(frame_padre, text="Detalles de ingresos", font=FUENTE_FORMULARIO_T).pack(pady=30)
    
    # Contenedor para la tabla
    contenedor_tabla = ctk.CTkFrame(frame_padre)
    contenedor_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    ## Frame contenedor para Treeview y scrollbar - usar tk.Frame con fondo oscuro manual
    modo = ctk.get_appearance_mode()
    if modo == "Dark":
        color_fondo = "#1e1e1e"
    else:
        color_fondo = "white"

    frame_tree = tk.Frame(contenedor_tabla, bg=color_fondo)  # Aquí sí se puede usar bg
    frame_tree.pack(fill="both", expand=True)
    
    columnas = ("fecha", "Poliza", "banco", "importe", "nota")
    estilo_tabla()
    
    estilo_act = "Dark.Treeview" if modo == "Dark" else "Light.Treeview"
    tabla = ttk.Treeview(frame_tree, columns=columnas, show="headings", style=estilo_act)
    
    anchos = {
        "fecha": 135,     # Fecha (dd/mm/yyyy)
        "Poliza": 135,    # Número de póliza
        "banco": 150,     # Nombre del banco
        "importe": 150,   # Valor numérico
        "nota": 250       # Notas (más ancho por texto variable)
    }

    # Manejar color de fondo del widget según modo
    if modo == "Dark":
        tabla.tk_setPalette(background="#1e1e1e")
    else:
        tabla.tk_setPalette(background="white")
    
    #for col in columnas:
    #    tabla.heading(col, text=col.capitalize())
    #    tabla.column(col, anchor="w", width=100)
    
    for col in columnas:
        # Configurar cabecera
        tabla.heading(col, text=col.capitalize())
    
        # Configurar propiedades de columna
        tabla.column(
            col, 
            anchor="w",              # Alineación (w=izquierda)
            width=anchos[col],       # Ancho personalizado
            minwidth=100,             # Ancho mínimo al redimensionar
            stretch=True if col == "nota" else False  # Solo "nota" se expande
        )
        
    tabla.update_idletasks()  # Actualiza cálculos de layout
    contenedor_tabla.update()  # Asegura que el contenedor padre se actualice
    # Modifica solo para la columna "importe"
    tabla.column("importe", anchor="e")  # "e" = right align
    
    #print("Anchos configurados:")
    #for col in columnas:
    #    print(f"{col}: {tabla.column(col, 'width')}px")   
    #print(f"Ancho disponible: {frame_tree.winfo_width()}px")




    tabla.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tabla.yview)
    scrollbar.pack(side="right", fill="y")

    tabla.configure(yscrollcommand=scrollbar.set)

    # Conectar a la base de datos
    conexion = sqlite3.connect("prueba.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, fecha, noPoliza, banco, importe, nota FROM polizasIngresos ORDER BY STRFTIME('%Y-%m-%d', SUBSTR(fecha, 7, 4) || '-' || SUBSTR(fecha, 4, 2) || '-' || SUBSTR(fecha, 1, 2)) DESC")
    registros = cursor.fetchall()
    # Imprimirlos en consola
    #for fila in registros:
    #    id, fecha, noPoliza, banco, importe, nota = fila
    #    print(f"ID: {id} | Fecha: {fecha} | Póliza: {noPoliza} | Banco: {banco} | Importe: {importe} | Nota: {nota}")
    conexion.close()

    if not registros:
        ctk.CTkLabel(contenedor_tabla, text="No hay registros.", font=("Arial", 14)).pack(pady=20)
        return

    # Insertar registros
    for fila in registros:
        id_registro = fila[0]
        valores_visibles = fila[1:]
        tabla.insert("", "end", values=valores_visibles, iid=id_registro)

    # Botones para editar y eliminar seleccionados
    frame_botones = ctk.CTkFrame(frame_padre)
    frame_botones.pack(pady=10)

    def obtener_seleccion():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "¡Selecciona un registro!")
            return None
        valores = tabla.item(seleccionado)["values"]
        id_registro = seleccionado
        return [id_registro] + valores

    btn_editar = ctk.CTkButton(frame_botones, text="Editar seleccionado", command=lambda: (
        (datos := obtener_seleccion()) and editar_registro(*datos, frame_padre)
    ))
    btn_editar.pack(side="left", padx=10)

    btn_eliminar = ctk.CTkButton(frame_botones, text="Eliminar seleccionado", fg_color="red", hover_color="darkred",
        command=lambda: (
            (datos := obtener_seleccion()) and eliminar_registro(datos[0], frame_padre)
    ))
    btn_eliminar.pack(side="left", padx=10)

    # Eliminar registro
def eliminar_registro(id_registro, frame_padre):
    confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este registro?")
    if confirm:
        conexion = sqlite3.connect("prueba.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM polizasIngresos WHERE id = ?", (id_registro,))
        conexion.commit()
        conexion.close()
        mostrar_detalles_ingresos(frame_padre)  # Refrescar vista
        
# Editar registro
def editar_registro(id_registro, fecha_antigua, no_poliza_ant, banco_ant, importe_ant, nota_ant, frame_padre):
    ventana_editar = ctk.CTkToplevel()
    ventana_editar.title("Editar Registro")
    ventana_editar.geometry("400x400")
    
    entradas = {}
    
    campos = {
        "Fecha (dd/mm/yyyy)": fecha_antigua,
        "No. Póliza": no_poliza_ant,
        "Banco": banco_ant,
        "Importe": str(importe_ant),
        "Nota": nota_ant,
    }

    for campo, valor in campos.items():
        ctk.CTkLabel(ventana_editar, text=campo + ":").pack(pady=(10, 0))
        entrada = ctk.CTkEntry(ventana_editar)
        entrada.insert(0, valor)
        entrada.pack()
        entradas[campo] = entrada

    def guardar():
        nueva_fecha = entradas["Fecha (dd/mm/yyyy)"].get()
        nuevo_poliza = entradas["No. Póliza"].get()
        nuevo_banco = entradas["Banco"].get()
        nuevo_importe = entradas["Importe"].get()
        nueva_nota = entradas["Nota"].get()


        conexion = sqlite3.connect("prueba.db")
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE polizasIngresos
            SET fecha = ?, noPoliza = ?, banco = ?, importe = ?, nota = ?
            WHERE id = ?
        """, (nueva_fecha, nuevo_poliza, nuevo_banco, nuevo_importe, nueva_nota, id_registro))
        conexion.commit()
        conexion.close()
        ventana_editar.destroy()
        mostrar_detalles_ingresos(frame_padre)

    ctk.CTkButton(ventana_editar, text="Guardar cambios", command=guardar).pack(pady=20)
    
def actualizar_estilo_tabla(tabla):
    modo = ctk.get_appearance_mode()
    estilo_act = "Dark.Treeview" if modo == "Dark" else "Light.Treeview"
    tabla.configure(style=estilo_act)    

def estilo_tabla():
    style = ttk.Style()
    style.theme_use("clam")  # Tema más flexible

    # Modo claro
    style.configure("Light.Treeview",
        background="white",
        foreground="black",
        fieldbackground="white",  # ¡Nuevo! Fondo de celdas
        rowheight=30,
        font=("Arial", 16)
    )
    
    # Modo oscuro
    style.configure("Dark.Treeview",
        background="#1e1e1e",
        foreground="white",
        fieldbackground="#1e1e1e",  # ¡Nuevo! Fondo de celdas
        rowheight=30,
        font=("Arial", 16)
    )

    # Heading (igual que antes, bien definido)
    style.configure("Light.Treeview.Heading",
        background="#f0f0f0",
        foreground="black",
        font=("Arial", 20, "bold")
    )
    style.configure("Dark.Treeview.Heading",
        background="#333333",
        foreground="white",
        font=("Arial", 20, "bold")
    )

    # Mapeo mejorado (incluye estado normal y selección)
    style.map("Light.Treeview",
        background=[("selected", "#cce5ff"), ("!selected", "white")],  # ¡Corregido!
        foreground=[("selected", "black"), ("!selected", "black")]
    )
    style.map("Dark.Treeview",
        background=[("selected", "#3a3a3a"), ("!selected", "#1e1e1e")],  # ¡Corregido!
        foreground=[("selected", "white"), ("!selected", "white")]
    )


    

    
    