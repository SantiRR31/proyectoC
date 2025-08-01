from datetime import datetime
import traceback
from typing import Self
import customtkinter as ctk
from db.egresosDB import cambiar_estado_poliza_id, consultar_poliza_por_no, eliminar_poliza, obtener_poliza_completa, obtener_polizas_egresos_filtrado
from informes.poliza import guardar_pdf, guardar_polizas_mes
from styles.styles import FUENTE_FORMULARIO_T
from tkinter import messagebox, ttk
from ui.egresos import mostrar_formulario_egresos
from utils.egresos_utils import mostrar_loading_y_ejecutar

def crear_treeview_polizas(parent, modo_tema="light"):
    columnas = ("no_poliza", "fecha", "nombre", "monto", "tipo de pago", "estado")

    # Estilos
    style = ttk.Style()
    style.theme_use("default")
    
    if modo_tema == "dark":
        fondo = "#2e2e2e"
        texto = "#ffffff"
        encabezado = "#444444"
        seleccionado = "#007acc"
        fila_activa = "#334455"
    else:
        fondo = "#f5f5f5"
        texto = "#333333"
        encabezado = "#007acc"
        seleccionado = "#005f99"
        fila_activa = "#e6f2ff"
        
    style.configure("Treeview",
                    background=fondo,
                    foreground=texto,
                    rowheight=30,
                    fieldbackground=fondo,
                    font=("Arial", 12))
    style.configure("Treeview.Heading",
                    background=encabezado,
                    foreground="white",
                    font=("Arial", 13, "bold"))
    style.map("Treeview", background=[("selected", seleccionado)])

    frame_tree = ctk.CTkFrame(parent)
    frame_tree.pack(fill="both", expand=True)

    # Scrollbar
    scroll_y = ttk.Scrollbar(frame_tree, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    tree = ttk.Treeview(frame_tree, columns=columnas, show="headings", height=10, yscrollcommand=scroll_y.set)
    scroll_y.config(command=tree.yview)

    for col in columnas:
        tree.heading(col, text=col.upper())
        tree.column(col, anchor="center", width=140)
        
        tree.tag_configure("activo", background="#ccffcc" if modo_tema == "light" else "#3a553a")
        tree.tag_configure("cancelado", background="#ffcccc" if modo_tema == "light" else "#553a3a")


    tree.pack(fill="both", expand=True)
    return tree

def mostrar_detalles_egresos(frame_padre):
    for widget in frame_padre.winfo_children():
        widget.destroy()

    ctk.CTkLabel(frame_padre, text="Detalles de egresos", font=FUENTE_FORMULARIO_T).pack(pady=20)

    # Filtros
    frame_filtros = ctk.CTkFrame(frame_padre)
    frame_filtros.pack(pady=10)

    meses = [f"{i:02d} - {nombre}" for i, nombre in enumerate([
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ], start=1)]

    anios = [str(anio) for anio in range(2020, datetime.now().year + 1)]

    combo_mes = ctk.CTkComboBox(frame_filtros, values=meses, width=160)
    combo_mes.pack(side="left", padx=10)

    combo_anio = ctk.CTkComboBox(frame_filtros, values=anios, width=100)
    combo_anio.pack(side="left", padx=10)

    boton_filtrar = ctk.CTkButton(frame_filtros, text="Filtrar", command=lambda: cargar_polizas())
    boton_filtrar.pack(side="left", padx=10)
    
        # Cada vez que se cambia el valor del mes o año, se recarga automáticamente
    combo_mes.bind("<<ComboboxSelected>>", lambda event: cargar_polizas())
    combo_anio.bind("<<ComboboxSelected>>", lambda event: cargar_polizas())


    contenedor_tabla = ctk.CTkFrame(frame_padre)
    contenedor_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        # Detectar modo
    modo_tema = ctk.get_appearance_mode().lower()  # "dark" o "light"
    tree = crear_treeview_polizas(contenedor_tabla, modo_tema)


    def cargar_polizas():
        tree.delete(*tree.get_children())
        mes = combo_mes.get().split(" - ")[0] if combo_mes.get() else None
        anio = combo_anio.get()
        mes = mes if mes != "Mes" else None
        anio = anio if anio != "Año" else None

        filas = obtener_polizas_egresos_filtrado(mes, anio)
        if not filas:
            tree.insert("", "end", values=("No hay datos disponibles", "", "", "", ""))
            return
    
        for fila in filas:
            id_poliza = fila[0]
            datos_visibles = fila[1:]  # Excluye el ID
            estado = datos_visibles[-1]
            tag = "activo" if estado and estado.lower() == "activo" else "cancelado"
            tree.insert("", "end", iid=str(id_poliza), values=datos_visibles, tags=(tag,))

    def cambiar_estado_poliza():
        seleccionado = tree.focus()
        if not seleccionado:
            return
        id_poliza = int(seleccionado)
        estado_actual = tree.item(seleccionado, "values")[5] 
        nuevo_estado = "cancelado" if estado_actual.lower() == "activo" else "activo"
        from tkinter import messagebox
        if not messagebox.askyesno("Confirmar", f"¿Deseas marcar esta póliza como '{nuevo_estado}'?"):
            return
        cambiar_estado_poliza_id(id_poliza,nuevo_estado)
        cargar_polizas()
        
    

    def editar_poliza():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona una póliza para editar.")
            return
        id_poliza = int(seleccionado)
        poliza = obtener_poliza_completa(id_poliza) 
        # Limpiar el frame y mostrar el formulario
        for widget in frame_padre.winfo_children():
            widget.destroy()

        ctk.CTkLabel(frame_padre, text=f"Editar Póliza {poliza.no_poliza}", font=FUENTE_FORMULARIO_T).pack(pady=10)

        mostrar_formulario_egresos(frame_padre, poliza_editar=poliza)
        
    def borrar_poliza():
        selecciondo = tree.focus()
        if not selecciondo:
            messagebox.showwarning("Advertencia", "Selecciona una póliza para borrar.")
            return

        id_poliza = int(selecciondo)

        confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de eliminar la póliza ID {id_poliza}? Esta acción no se puede deshacer.")
        if not confirmar:
            return

        try:
            eliminar_poliza(id_poliza)
            tree.delete(selecciondo)  # Elimina visualmente del Treeview
            messagebox.showinfo("Éxito", "Póliza eliminada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la póliza.\nDetalles: {e}")
            
    def guardar_mes(mes, anio):
        if not mes or not anio:
            messagebox.showwarning("Advertencia", "Selecciona un mes y año válidos.")
            return
        try:
            mes_num = int(mes.split(" - ")[0])
            anio_num = int(anio)
            guardar_polizas_mes(parent=frame_padre, mes=mes_num, anio=anio_num) 
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar las pólizas del mes.\nDetalles: {e}")
    
    def guardar_seleccionada():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona una póliza para guardar.")
            return

        no_poliza = tree.item(seleccionado)['values'][0]  # Asumiendo que no_poliza está en la primera columna
        try:
            poliza = consultar_poliza_por_no(no_poliza)
            if poliza is None:
                messagebox.showerror("Error", f"No se encontró la póliza con número: {no_poliza}")
                return
            mostrar_loading_y_ejecutar(guardar_pdf, contenedor_principal=frame_padre, poliza=poliza)
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo guardar la póliza como PDF.\n\nDetalles: {e}")


        
    boton_frame = ctk.CTkFrame(frame_padre, fg_color="transparent")
    boton_frame.pack(side="bottom", fill="x", pady=10)

    boton_estado = ctk.CTkButton(
        boton_frame,
        text="Cambiar Estado",
        command=cambiar_estado_poliza,
        fg_color="#ffaa00",
        hover_color="#cc8800",
        width=140
    )
    boton_estado.pack(side="left", padx=10)

    boton_editar = ctk.CTkButton(
        boton_frame,
        text="Editar",
        command=editar_poliza,
        fg_color="#005f99",  # Azul profundo
        hover_color="#004d80",
        width=140
    )
    boton_editar.pack(side="left", padx=10)

    boton_borrar = ctk.CTkButton(
        boton_frame,
        text="Borrar",
        command=borrar_poliza,
        fg_color="#ff4500",
        hover_color="#cc3700",
        width=140
    )
    boton_borrar.pack(side="left", padx=10)
    
    boton_guardar_mes = ctk.CTkButton(
        boton_frame,
        text="Guardar polizas del mes",
        command=lambda: guardar_mes(combo_mes.get(), combo_anio.get()),
        fg_color="#007acc",
        hover_color="#005f99",
        width=180
    )
    boton_guardar_mes.pack(side="left", padx=10)
    
    boton_guardar_seleccion = ctk.CTkButton(
        boton_frame,
        text="Guardar poliza seleccionada",
        command=guardar_seleccionada,
        fg_color="#007acc",
        hover_color="#005f99",
        width=180
    )
    boton_guardar_seleccion.pack(side ="left", padx =10)


    # Establecer por defecto el mes y año actuales antes de cargar
    mes_actual = datetime.now().strftime("%m")
    anio_actual = datetime.now().strftime("%Y")
    mes_actual_str = [m for m in meses if m.startswith(mes_actual)][0]
    combo_mes.set(mes_actual_str)
    combo_anio.set(anio_actual)

    cargar_polizas()
    
    
    
