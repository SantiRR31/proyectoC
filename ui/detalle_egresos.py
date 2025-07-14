from datetime import datetime
import customtkinter as ctk
from db.egresosDB import cancelar_poliza_por_id, obtener_polizas_egresos, obtener_polizas_egresos_filtrado
from styles.styles import FUENTE_FORMULARIO_T
from tkinter import ttk

def crear_treeview_polizas(parent):
    columnas = ("no_poliza", "fecha", "monto", "nombre", "estado")
    tree = ttk.Treeview(parent, columns=columnas, show="headings", height=15)

    for col in columnas:
        tree.heading(col, text=col.upper())
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True)
    return tree

def mostrar_detalles_egresos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()

    ctk.CTkLabel(frame_padre, text="Detalles de egresos", font=FUENTE_FORMULARIO_T).pack(pady=20)

    # Filtros
    frame_filtros = ctk.CTkFrame(frame_padre)
    frame_filtros.pack(pady=10)

    meses = [f"{i:02d}" for i in range(1, 13)]
    anios = [str(anio) for anio in range(2020, datetime.now().year + 1)]

    combo_mes = ctk.CTkComboBox(frame_filtros, values=meses, width=80)
    combo_mes.set("Mes")
    combo_mes.pack(side="left", padx=10)

    combo_anio = ctk.CTkComboBox(frame_filtros, values=anios, width=100)
    combo_anio.set("Año")
    combo_anio.pack(side="left", padx=10)

    boton_filtrar = ctk.CTkButton(frame_filtros, text="Filtrar", command=lambda: cargar_polizas())
    boton_filtrar.pack(side="left", padx=10)

    contenedor_tabla = ctk.CTkFrame(frame_padre)
    contenedor_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    tree = crear_treeview_polizas(contenedor_tabla)

    def cargar_polizas():
        tree.delete(*tree.get_children())
        mes = combo_mes.get()
        anio = combo_anio.get()
        mes = mes if mes != "Mes" else None
        anio = anio if anio != "Año" else None

        filas = obtener_polizas_egresos_filtrado(mes, anio)
        for fila in filas:
            id_poliza = fila[0]
            datos_visibles = fila[1:]  # Excluye el ID
            tree.insert("", "end", iid=str(id_poliza), values=datos_visibles)

    def cancelar_poliza():
        seleccionado = tree.focus()
        if not seleccionado:
            return
        id_poliza = int(seleccionado)
        cancelar_poliza_por_id(id_poliza)
        cargar_polizas()

    boton_cancelar = ctk.CTkButton(
        frame_padre,
        text="Cancelar Póliza Seleccionada",
        command=cancelar_poliza,
        fg_color="red",
        hover_color="#aa0000"
    )
    boton_cancelar.pack(pady=10)

    cargar_polizas()
